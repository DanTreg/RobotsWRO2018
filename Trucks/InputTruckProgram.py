#!/usr/bin/env python3

import time
import paho.mqtt.client as mqtt
from threading import Thread
from ev3dev.ev3 import *
import requests
import json
import random

urlGetbyPlace= 'http://192.168.0.109/api/v2/products/getbyplace'
urlMove = 'http://192.168.0.109/api/v2/products/move'
headers = {'content-type': 'application/json'}

ProductName = None
Freshness = None

msgFromEV3 = ""
class ListenEV3(Thread):
    
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener.connect("192.168.0.110",1883,60)
        listener.on_connect = self.on_connect
        listener.on_message = self.on_message
        print("client is created")
    
    def run(self):
        print("thread start")
        listener.loop_forever()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        listener.subscribe("ev3/to/car")
        print("I am listening to EV3")

    def on_message(self, client, userdata, msg):
        global msgFromEV3
        msgFromEV3 = msg.payload.decode()
        print("EV3 says: " + msgFromEV3)



def product_move(ProductName, Freshness, Place):
    tochoosefrom=["True","False"]
    data={}
    data["RobotName"] = 3
    data["ProductName"]=ProductName
    data["Place"]=Place
    data["Freshness"]=Freshness
    data["Temperature"]=random.choice(tochoosefrom)

    data_r=json.dumps(data)
    print('data_r: ', data_r)
    r=requests.post(urlMove,headers=headers, data=data_r)
    print('response: ',r)


def getByPlace(Place):
    global ProductName
    global Freshness
    tochoosefrom = ["True", "False"]
    data = {}
    data["Place"] = Place

    data_r = json.dumps(Place)
    print('data_r: ', data_r)
    r = requests.post(urlGetbyPlace, headers=headers, data=data_r)

    p = r.text
    print('resp.responseonse: ', p)
    p = json.loads(p)

    print(p['ProductName'])
    print(p['Freshness'])
    ProductName = p['ProductName']
    if p['Freshness'] == 2:
        Freshness = 'True'
    if p['Freshness'] == 4:
        Freshness = 'False'
    print('response: ',r)



listener = mqtt.Client()
sender = mqtt.Client()

my_thread = ListenEV3("Listen to PC")
my_thread.start()

sender.connect("192.168.0.110",1883,1000)

m = LargeMotor('outB')
ts4 = TouchSensor('in1')
assert ts4.connected, "Connect a touch sensor to sensor port 4"


def main(): #основная функция
    try:
        flag = 0
        global msgFromEV3
        while True:  # Stop this program with Ctrl-C
            if ts4.value() == 1:
                print("ts1")
                sender.publish("car/to/ev3", 'input')
                msgFromEV3 = ''
                print('done ts1')
                time.sleep(1)
            if msgFromEV3 == 'get' and flag == 0:

                m.run_to_rel_pos(position_sp=-500, speed_sp=150, stop_action='brake')
                time.sleep(2)
                getByPlace(12)
                time.sleep(2)
                product_move(ProductName, Freshness, 11)
                msgFromEV3 = ""
                flag = 1
            if msgFromEV3 == 'get' and flag == 1:
                pass


    finally:
        listener.disconnect()
        m.stop(stop_action='brake')


main()
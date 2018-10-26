#!/usr/bin/env python3

import time
import paho.mqtt.client as mqtt
from threading import Thread
from ev3dev.ev3 import *
import json
import requests
import random
from time import sleep

urlGetbyPlace= 'http://192.168.0.109/api/v2/products/getbyplace'
urlMove = 'http://192.168.0.109/api/v2/products/move'
headers = {'content-type': 'application/json'}

ProductName = None
Freshness = None


msgFromEV4 = ""
class ListenEV4(Thread):
    
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
        listener.subscribe("ev4/to/car")
        print("I am listening to EV4")

    def on_message(self, client, userdata, msg):
        global msgFromEV4
        msgFromEV4 = msg.payload.decode()
        print("EV4 says: " + msgFromEV4)


def product_move(ProductName, Freshness, Place):
    tochoosefrom=["True","False"]
    data={}
    data["RobotName"] = 4
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
    if p['Freshness'] == 3:
        Freshness = 'True'
    print('response: ',r)


listener = mqtt.Client()
sender = mqtt.Client()

my_thread = ListenEV4("Listen to PC")
my_thread.start()

sender.connect("192.168.0.110",1883,1000)

m = LargeMotor('outA')
mD = MediumMotor('outD')
ts4 = TouchSensor('in4')
assert ts4.connected, "Connect a touch sensor to sensor port 4"



def main(): #основная функция
    try:
        global msgFromEV4
        flag = 0
        while True:  # Stop this program with Ctrl-C
            if ts4.value() == 1:
                print("ts4")
                sender.publish("car/to/ev4", 'output')
                print('done ts2')
                time.sleep(1)
            if msgFromEV4 == "put" and flag == 0:
                mD.run_to_rel_pos(position_sp=70, speed_sp=150, stop_action='brake')
                mD.wait_while('running')
                mD.stop(stop_action='brake')
                print('down')
                time.sleep(6)
                m.run_to_rel_pos(position_sp=500, speed_sp=150, stop_action='brake')

                m.wait_while('running')
                m.stop(stop_action='brake')
                print('move')
                mD.run_to_rel_pos(position_sp=-70, speed_sp=150, stop_action='brake')
                mD.wait_while('running')
                getByPlace(13)
                product_move(ProductName,Freshness,14)
                mD.stop(stop_action='brake')
                print('up')
                flag=1
                msgFromEV4 = ""
            if msgFromEV4 == "put" and flag == 1:
                mD.run_to_rel_pos(position_sp=70, speed_sp=150, stop_action='brake')
                mD.wait_while('running')
                mD.stop(stop_action='brake')
                time.sleep(10)
                mD.run_to_rel_pos(position_sp=-70, speed_sp=150, stop_action='brake')
                mD.wait_while('running')
                mD.stop(stop_action='brake')


            msgFromEV4 = ""
    finally:
        listener.disconnect()
        m.stop(stop_action='brake')
        mD.stop(stop_action='brake')
    

main()

import paho.mqtt.client as mqtt
from threading import Thread
from ev3dev.ev3 import *


listener_pc = mqtt.Client()
listener_car = mqtt.Client()
listener_pi = mqtt.Client()
sender = mqtt.Client()

msgFromPC = ""
msgFromCar = ""
msgFromPi = ""

class ListenPC(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_pc.connect("192.168.0.110", 1883, 60)
        listener_pc.on_connect = self.on_connect
        listener_pc.on_message = self.on_message
        print("client is created")

    def run(self):
        print("pc_thread start")
        listener_pc.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_pc.subscribe("pc/to/ev4")
        print("I am listening to pc")

    def on_message(self, client, userdata, msg):
        global msgFromPC
        msgFromPC = msg.payload.decode()
        print("pc says: " + msgFromPC)


class ListenPi(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_pi.connect("192.168.0.110", 1883, 60)
        listener_pi.on_connect = self.on_connect
        listener_pi.on_message = self.on_message
        print("client is created")

    def run(self):
        print("pi_thread start")
        listener_pi.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_pi.subscribe("pi/to/ev4")
        print("I am listening to pi")

    def on_message(self, client, userdata, msg):
        global msgFromPi
        msgFromPi = msg.payload.decode()
        print("pi says: " + msgFromPi)


class ListenCar(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener_car.connect("192.168.0.110", 1883, 60)
        listener_car.on_connect = self.on_connect
        listener_car.on_message = self.on_message
        print("client is created")

    def run(self):
        print("car_thread start")
        listener_car.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        listener_car.subscribe("car/to/ev4")
        print("I am listening to car")

    def on_message(self, client, userdata, msg):
        global msgFromCar
        msgFromCar = msg.payload.decode()
        print("car says: " + msgFromCar)
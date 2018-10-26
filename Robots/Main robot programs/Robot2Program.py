#!/usr/bin/env python3

import time
import math
import paho.mqtt.client as mqtt
from threading import Thread
from ev3dev.ev3 import *
from time import sleep
from listenerout import *
import listenerout as ls
import tools
import manipulator as mp

mA = MediumMotor('outA')
mB = MediumMotor('outB')
mC = MediumMotor('outC')
mD = LargeMotor('outD')
ts1 = TouchSensor('in1')
assert ts1.connected; "Connect a touch sensor to sensor port 1"
ts2 = TouchSensor('in2')
assert ts2.connected; "Connect a touch sensor to sensor port 1"
f=0

def init():
    mp.go(0)
    mp.go(0,'init')
    print('send test')  # отправить ready в базу данных
     # на этом месте должен быть запрос в БД
    while ls.msgFromPC != 'ok':
        sender.publish("ev4/to/pc", 'test')
        print(ls.msgFromPC)
        sleep(5)
    ls.msgFromPC = ''

def move_oracul(command):
    while True:
        sender.publish("ev4/to/pc", command)
        while ls.msgFromPC == '':
            continue
            #print("wait from PC")
            #sleep(2)
        print('ls.msgFromPC= '+ ls.msgFromPC)
        data=tools.find_int(ls.msgFromPC)
        #a = int(re.findall(r'a(\d+)', ls.msgFromPC)[0])  # Угол
        #d = int(re.findall(r'd(\d+)', ls.msgFromPC)[0])  # Дистанция
        a = data[0]
        d = data[1]
        #print(a)
        #print(d)
        if a == 1000 and d == 1000:
            print("STOOOOOP")
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            continue
        if a == 0 and d == 0:
            ls.msgFromPC = ''
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            print('exit')# Выход из цикла
            break
        if d == 0:  # Если дистанция равна 0, то поворачивает на какой-то угол влево или вправо
            mA.run_to_rel_pos(position_sp=a * 4.4, speed_sp=300, stop_action="brake")
            mB.run_to_rel_pos(position_sp=a * 4.4, speed_sp=300, stop_action="brake")
            mC.run_to_rel_pos(position_sp=a * 4.4, speed_sp=300, stop_action="brake")
            mA.wait_while('running')
            mB.wait_while('running')
            mC.wait_while('running')
            #sleep(1)
            #print('d=0 done')
        else:  # Иначе едет на какое-то расстояние, на какой-то угол
            # if (d>200):
            #     power = 30
            # elif(d<=200 and d>100):
            #     power = 15
            # else:
            #     power = 5
            power=d*0.45
            #print('power='+str(power))
            if power>100:
                power=100
            a_r = math.radians(a)  # перевод угла в радианы
            y = round(math.cos(a_r), 2)
            x = round(math.sin(a_r), 2)
            ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
            n = [-x, y, 0]
            c = [0, 0, 0]
            c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
            c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
            c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
            #print(c)
            c[0] = c[0] * 10
            c[1] = c[1] * 10
            c[2] = c[2] * 10
            mA.run_forever(speed_sp=c[0])
            mB.run_forever(speed_sp=c[1])
            mC.run_forever(speed_sp=c[2])
            #mA.run_timed(time_sp=d, speed_sp=c[0])
            #mB.run_timed(time_sp=d, speed_sp=c[1])
            #mC.run_timed(time_sp=d, speed_sp=c[2])
            #mA.wait_while('running')
            #mB.wait_while('running')
            #mC.wait_while('running')
            #sleep(1)
            #print('d!=0 done')
        ls.msgFromPC=''
        #sleep(0.8)
    sender.publish("ev4/to/pc", "ok")

def move_Pi(command):
    global f

    sender.publish("ev4/to/pi", command)
    sleep(0.2)
    while True:
        while ls.msgFromPi == '':
            time.sleep(0.01)
            #print("wait from Pi")
        print('ls.msgFromPi= '+ ls.msgFromPi+'!')
        data=tools.find_int(ls.msgFromPi)
        a = data[0]
        d = data[1]
        print(a)
        print(d)
        if a == 0 and d == 0:
            ls.msgFromPi = ''
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            print('exit')# Выход из цикла
            break
        if a == 1000 and d == 1000:
            print("STOOOOOP")
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            f=1
            return f
        elif d == 0:  # Если дистанция равна 0, то поворачивает на какой-то угол влево или вправо
            # mA.run_to_rel_pos(position_sp=a * 4.4, speed_sp=500, stop_action="brake")
            # mB.run_to_rel_pos(position_sp=a * 4.4, speed_sp=500, stop_action="brake")
            # mC.run_to_rel_pos(position_sp=a * 4.4, speed_sp=500, stop_action="brake")
            # mA.wait_while('running')
            # mB.wait_while('running')
            # mC.wait_while('running')
            #sleep(1)
            print('d=0 done')
        else:  # Иначе едет на какое-то расстояние, на какой-то угол
            power = d*0.35
            if power > 170:
                power = 170
            if power < 25:
                power = 25
            #coef = d*0.1
            #print("coef=", str(coef))
            a_r = math.radians(a)  # перевод угла в радианы
            y = round(math.cos(a_r), 2)
            x = round(math.sin(a_r), 2)
            ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
            n = [-x, y, 0]
            c = [0.0, 0.0, 0.0]
            c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
            c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
            c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
            # c[0] = c[0] * 10
            # c[1] = c[1] * 10
            # c[2] = c[2] * 10
            print(c)
            mA.run_forever(speed_sp=c[0])
            mB.run_forever(speed_sp=c[1])
            mC.run_forever(speed_sp=c[2])
            # mA.run_timed(time_sp=1000, speed_sp=c[0])
            # mB.run_timed(time_sp=1000, speed_sp=c[1])
            # mC.run_timed(time_sp=1000, speed_sp=c[2])
            # mA.wait_while('running')
            # mB.wait_while('running')
            # mC.wait_while('running')
            # mA.stop(stop_action="brake")
            # mB.stop(stop_action="brake")
            # mC.stop(stop_action="brake")
            print('move pi d!=0 done')
            #sleep(0.5)
        ls.msgFromPi=''
    print('send pi ok')
    sender.publish("ev4/to/pi", "ok")

pc_thread = ListenPC("Listen to PC")
car_thread = ListenCar("Listen to Car")
pi_thread = ListenPi("Listen to Pi")

pc_thread.start()
car_thread.start()
pi_thread.start()
sender.connect("192.168.0.110",1883,1000)


def main(): #основная функция
    global f
    try:
        init()
        while True:
            whereToGoArrayUtill = tools.find_sklad_util()
            if whereToGoArrayUtill != [0,0]:
                ls.msgFromCar = 'util'
            if ls.msgFromCar == 'input':
                print('ls.msgFromCar = ' + ls.msgFromCar)
                ls.msgFromCar=''
                sleep(1)
                sender.publish("ev3/to/car", 'ok')
                print('send to car ok')
                move_oracul('input')     #приехали в input
                #mp.go(1, input)
                #sleep(1.5)
                #mp.go(0)
                #print("we are down on the floor")
                mp.go(1, 'input')
                print("we are ggeting product from input")
                move_Pi('adjust')
                print("just adjusted")
                sender.publish("ev3/to/pi", 'readQR')
                time.sleep(3)
                mp.move_forwardout()
                print("moving forward")
                mp.go(2,'up')
                print("lifting a bit")
                mp.move_backward()
                print("getting back")
                mp.go(2,"drop")
                sender.publish("ev3/to/car", 'get')
                sender.publish("ev3/to/pi", 'readGAZ')
                while True:
                    print('Ready to post product move ', ls.msgFromPi)
                    if ls.msgFromPi != '':
                        a = ls.msgFromPi
                        l = a.split(' ')
                        ProductName = l[0]
                        Freshness = l[1]
                        ls.msgFromPi = ''
                        break
                time.sleep(1)
                tools.product_move(ProductName,Freshness,9,1)
                whereToGoArray=tools.find_sklad_input()
                if whereToGoArray[0]==0:
                    #  поехали в sklad1
                    move_oracul('sklad1')
                    move_Pi('adjust')
                    Place=-1
                if whereToGoArray[0] == 1:
                       #  поехали в sklad1
                    move_oracul('sklad2')
                    move_Pi('adjust')
                    Place=2
                if whereToGoArray[0] == 2:
                   #  поехали в sklad1
                    move_oracul('sklad3')
                    move_Pi('adjust')
                    Place=5
                mp.go(whereToGoArray[1]+1,"put")
                mp.move_forward()
                mp.go(whereToGoArray[1]+1,"drop")
                mp.move_backward()
                tools.product_move(ProductName,Freshness,Place+whereToGoArray[1]+1,1)
                move_oracul('input')

             #mp.go(1,'put')
            elif ls.msgFromCar == 'output':
                print('msgFromCar = ' + ls.msgFromCar)
                ls.msgFromCar=''
                sleep(1)
                sender.publish("ev4/to/car", 'ok')
                #mp.go(0)
                mp.go(1, 'input')
                whereToGoArray=tools.find_sklad_output()
                print(whereToGoArray[0])
                aisleIsBusy=tools.verifyAisleIsBusy(whereToGoArray[0])
                while aisleIsBusy != "false":
                    aisleIsBusy=tools.verifyAisleIsBusy(whereToGoArray[0])
                    sleep(0.1)
                if whereToGoArray[0]==0:
                    #  поехали в sklad1
                    tools.isBusy(whereToGoArray[0], 'true')
                    move_oracul('sklad1')
                    move_Pi('adjust')
                    if f==1:
                        f=0
                        continue
                if whereToGoArray[0] == 1:
                    #  поехали в sklad1
                    tools.isBusy(whereToGoArray[0], 'true')
                    move_oracul('sklad2')
                    move_Pi('adjust')
                    if f==1:
                        f=0
                        continue
                if whereToGoArray[0] == 2:
                    #  поехали в sklad1
                    tools.isBusy(whereToGoArray[0], 'true')
                    move_oracul('sklad3')
                    move_Pi('adjust')
                    if f==1:
                        f=0
                        continue
                mp.go(whereToGoArray[1]+1,"get")
                #time.sleep(5)
                move_Pi('adjust')
                sender.publish("ev4/to/pi", 'readQR')
                time.sleep(5)
                mp.move_forwardoutt()
                mp.go(whereToGoArray[1]+1,"upp")
                mp.move_backwardout()
                sender.publish("ev4/to/pi", 'readGAZ')
                while True:
                    print('Ready to post product move ', ls.msgFromPi)
                    if ls.msgFromPi != '':
                        a = ls.msgFromPi
                        l = a.split(' ')
                        ProductName = l[0]
                        Freshness = l[1]
                        ls.msgFromPi = ''
                        break

                tools.product_move(ProductName, Freshness, 10, 2)
                #mp.go(0)
                mp.go(2,"350")
                mD.wait_while('running')
                tools.isBusy(whereToGoArray[0], 'false')
                move_oracul('output')    #приехали в output
                move_Pi('adjust1')

                #mp.go(0)
                mp.go(1, 'util')
                sleep(1.5)
                sender.publish("ev4/to/car", 'put')
                mp.move_forwardoutt()
                sleep(1)
                mp.go(1, "dropout")
                sleep(1)
                mp.move_backward()
                tools.product_move(ProductName, Freshness, 13, 2)
            elif ls.msgFromCar == 'util':
                sender.publish('ev3/to/util', 'gohere')
                print('ls.msgFromCar = ' + ls.msgFromCar)
                ls.msgFromCar=''
                #mp.go(0)
                mp.go(1, 'input')
                aisleIsBusy=tools.verifyAisleIsBusy(whereToGoArrayUtill[0])
                while aisleIsBusy != "false":
                    aisleIsBusy=tools.verifyAisleIsBusy(whereToGoArrayUtill[0])
                    sleep(0.1)
                if whereToGoArrayUtill[0]==0:
                    #  поехали в sklad1
                    tools.isBusy(whereToGoArrayUtill[0],'true')
                    move_oracul('sklad1')
                    print('im here')
                    move_Pi('adjust')
                if whereToGoArrayUtill[0] == 1:
                       #  поехали в sklad1
                    tools.isBusy(whereToGoArrayUtill[0],'true')
                    move_oracul('sklad2')
                    print('im here')
                    move_Pi('adjust')
                if whereToGoArrayUtill[0] == 2:
                   #  поехали в sklad1
                    tools.isBusy(whereToGoArrayUtill[0],'true')
                    move_oracul('sklad3')
                    print('im here')
                    move_Pi('adjust')
                mp.go(whereToGoArrayUtill[1]+1,"get")

                move_Pi('adjust')
                sender.publish("ev4/to/pi", 'readQR')
                time.sleep(5)
                mp.move_forwardout()
                mp.go(whereToGoArrayUtill[1]+1,"up")
                mp.move_backward()
                mp.go(2,'350')
                #mp.go(0)
                #mp.go(1,"up")
                sender.publish("ev4/to/pi", 'readGAZ')
                print("PRINTTTTTTTTTTTTTTTTTTT")
                time.sleep(2)
                while True:
                    print('Ready to post product move ', ls.msgFromPi)
                    print("PRINTTT")
                    if ls.msgFromPi != '':
                        a = ls.msgFromPi
                        l = a.split(' ')
                        ProductName = l[0]
                        Freshness = l[1]
                        ls.msgFromPi = ''
                        break

                tools.product_move(ProductName, Freshness, 10, 2)
                #mp.go(0)
                mp.go(1,'put')
                tools.isBusy(whereToGoArrayUtill[0], 'false')
                move_oracul('util')      #приехали в util
                move_Pi('adjust')
                #mp.go(0)
                mp.go(1, 'util')
                time.sleep(2)
                mp.move_forwardoutt()
                time.sleep(1)
                mp.go(1, "droputil")
                time.sleep(1.2)
                mp.move_backward()
                tools.product_move(ProductName, Freshness, 15, 2)
                sender.publish('ev3/to/util', 'ready')

    finally:
        print("finally")
        listener_pc.disconnect()
        listener_car.disconnect()
        listener_pi.disconnect()
        mA.stop(stop_action="brake")
        mB.stop(stop_action="brake")
        mC.stop(stop_action="brake")
        mD.stop(stop_action="brake")

main()
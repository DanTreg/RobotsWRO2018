#!/usr/bin/env python3

import time
import math
import paho.mqtt.client as mqtt
from threading import Thread
from ev3dev.ev3 import *
from time import sleep
from listenerint import *
import listenerint as ls
import tools
import manipulator as mp

RobotNumber = 1



mA = MediumMotor('outA')
mB = MediumMotor('outB')
mC = MediumMotor('outC')
mD = LargeMotor('outD')
ts1 = TouchSensor('in1')
assert ts1.connected; "Connect a touch sensor to sensor port 1"
ts2 = TouchSensor('in2')
assert ts2.connected; "Connect a touch sensor to sensor port 1"

def init():
    mp.go(0)
    mp.go(0,'init')
    sender.publish("ev3/to/pc", 'test')
    print('send test')  # отправить ready в базу данных
     # на этом месте должен быть запрос в БД
    sender.publish("ev3/to/pc", 'test')
    while ls.msgFromPC != 'ok':
        print(ls.msgFromPC)
        sleep(1)
    ls.msgFromPC = ''

def move_oracul(command):
    while True:
        #print('we are in move_oracul')
        sender.publish("ev3/to/pc", command)
        while ls.msgFromPC == '':
            continue
        print('ls.msgFromPC= '+ ls.msgFromPC)
        data=tools.find_int(ls.msgFromPC)
        #a = int(re.findall(r'a(\d+)', ls.msgFromPC)[0])  # Угол
        #d = int(re.findall(r'd(\d+)', ls.msgFromPC)[0])  # Дистанция
        a = data[0]
        d = data[1]
        #print(a)
        #print(d)
        if a == 1000 and d == 1000:
            print('STOOOOOOP')
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            sleep(1)
            continue
        if a == 0 and d == 0:
            ls.msgFromPC = ''
            mA.stop(stop_action="brake")
            mB.stop(stop_action="brake")
            mC.stop(stop_action="brake")
            print('exit')# Выход из цикла
            break
        if a!=0 and d == 0:  # Если дистанция равна 0, то поворачивает на какой-то угол влево или вправо
            power=300
            mA.run_to_rel_pos(position_sp=a * 4.4, speed_sp=power, stop_action="brake")
            mB.run_to_rel_pos(position_sp=a * 4.4, speed_sp=power, stop_action="brake")
            mC.run_to_rel_pos(position_sp=a * 4.4, speed_sp=power, stop_action="brake")
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
            print(c)
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
            #print('done')

        ls.msgFromPC=''
        #sleep(0.8)
        #print('test')
    sender.publish("ev3/to/pc", "ok")
    #print("ev3/to/pc    ok")

def move_Pi(command):
    sender.publish("ev3/to/pi", command)
    sleep(0.2)
    while True:
        while ls.msgFromPi == '':
            sleep(0.01)
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
        elif a!=0 and d == 0:  # Если дистанция равна 0, то поворачивает на какой-то угол влево или вправо
            # mA.run_to_rel_pos(position_sp=a * 4.4, speed_sp=500, stop_action="brake")
            # mB.run_to_rel_pos(position_sp=a * 4.4, speed_sp=500, stop_action="brake")
            # mC.run_to_rel_pos(position_sp=a * 4.4, speed_sp=500, stop_action="brake")
            # mA.wait_while('running')
            # mB.wait_while('running')
            # mC.wait_while('running')
            #sleep(1)
            print('d=0 done')
        else:  # Иначе едет на какое-то расстояние, на какой-то угол
            power = d*0.5
            if power > 160:
                power = 160
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
    sender.publish("ev3/to/pi", "ok")

pc_thread = ListenPC("Listen to PC")
car_thread = ListenCar("Listen to Car")
pi_thread = ListenPi("Listen to Pi")

pc_thread.start()
car_thread.start()
pi_thread.start()
sender.connect("192.168.0.110",1883,1000)


def main(): #основная функция
    try:
        init()
        while True:
            if ls.msgFromCar == 'input':
                print('ls.msgFromCar = ' + ls.msgFromCar)
                ls.msgFromCar=''
                sleep(1)
                sender.publish("ev3/to/car", 'ok')
                print('send to car ok')
                print('ready to move oracul')
                move_oracul('input')     #приехали в input
                #mp.go(1, input)
                #sleep(1.5)
                #mp.go(0)
                #print("we are down on the floor")
                mp.go(1, 'utilint')
                print("we are ggeting product from input")
                move_Pi('adjust')
                sender.publish("ev3/to/pi", 'ok')
                ls.msgFromPi = ''
                print("just adjusted")
                sender.publish("ev3/to/pi", 'readQR')
                time.sleep(3)
                mp.move_forwardin()
                print("moving forward")
                mp.go(2,'up')
                print("lifting a bit")
                mp.move_backward()
                print("getting back")
                mp.go(2,"drop")
                sender.publish("ev3/to/car", 'get')
                sender.publish("ev3/to/pi", 'readGAZ')
                mp.go(1, 'dropint')
                while True:
                    print('Ready to post product move ', ls.msgFromPi)
                    #time.sleep(1)
                    if ls.msgFromPi != '':
                        a = ls.msgFromPi
                        l = a.split(' ')
                        ProductName = l[0]
                        print(l)
                        Freshness = l[1]
                        ls.msgFromPi = ''
                        break
                tools.product_move(ProductName,Freshness,9,1)
                '''
                while True:
                    if ls.msgFromPi == '1':
                        ls.msgFromPi = ''
                        sender.publish("ev3/to/util",'gohere')
                        move_oracul('util')
                        mp.go(0)
                        mD.run_to_rel_pos(position_sp=200, speed_sp=500, stop_action="hold")
                        move_Pi('adjust1')
                        mp.go(0)
                        mp.go(1,'util')
                        sleep(1.5)
                        mp.move_forward()
                        mp.go(2,'drop')
                        mp.move_backward()
                        sender.publish("ev3/to/util",'ready')
                        flag = 2
                        break
                    if ls.msgFromPi == '0':
                        ls.msgFromPi = ''
                        flag=0
                        break
                if flag==2:
                    flag = 0
                    continue
                    '''

                whereToGoArray=tools.find_sklad_input()
                print(whereToGoArray[0])
                aisleIsBusy=tools.verifyAisleIsBusy(whereToGoArray[0])
                while aisleIsBusy != "false":
                    aisleIsBusy=tools.verifyAisleIsBusy(whereToGoArray[0])
                    sleep(0.5)
                if whereToGoArray[0]==0:
                    #  поехали в sklad1
                    tools.isBusy(whereToGoArray[0], 'true')
                    move_oracul('sklad1')
                    move_Pi('adjust')
                    Place=-1
                    sender.publish("ev3/to/pi", 'ok')
                    ls.msgFromPi = ''
                if whereToGoArray[0] == 1:
                       #  поехали в sklad1
                    tools.isBusy(whereToGoArray[0], 'true')
                    move_oracul('sklad2')
                    move_Pi('adjust')
                    Place=2
                    sender.publish("ev3/to/pi", 'ok')
                    ls.msgFromPi = ''
                if whereToGoArray[0] == 2:
                   #  поехали в sklad1
                    tools.isBusy(whereToGoArray[0], 'true')
                    move_oracul('sklad3')
                    move_Pi('adjust')
                    Place=5
                    sender.publish("ev3/to/pi", 'ok')
                    ls.msgFromPi = ''
                mp.go(whereToGoArray[1]+1,"put")
                mp.move_forward()
                mp.go(whereToGoArray[1]+1,"drop")
                mp.move_backward()
                tools.product_move(ProductName,Freshness,Place+whereToGoArray[1]+1,1)
                tools.isBusy(whereToGoArray[0], 'false')
                move_oracul('input')

             #mp.go(1,'put')
            elif ls.msgFromCar == 'output':
                print('msgFromCar = ' + ls.msgFromCar)
                ls.msgFromCar=''
                sleep(1)
                sender.publish("ev3/to/car", 'ok')
                mp.go(0)
                mp.go(1, 'input')
                whereToGoArray=tools.find_sklad_output()
                if whereToGoArray[0]==0:
                    #  поехали в sklad1
                    move_oracul('sklad1')
                    move_Pi('adjust')
                if whereToGoArray[0] == 1:
                    #  поехали в sklad1
                    move_oracul('sklad2')
                    move_Pi('adjust')
                if whereToGoArray[0] == 2:
                    #  поехали в sklad1
                    move_oracul('sklad3')
                    move_Pi('adjust')
                mp.go(whereToGoArray[1]+1,"get")
                mp.move_forward()
                mp.go(whereToGoArray[1]+1,"up")
                mp.move_backward()
                move_oracul('output')    #приехали в output
                move_Pi('adjust1')
                mp.go(0)
                mp.go(1, 'output')
                mp.move_forward()
                mp.go(2, "drop")
                mp.move_backward()
            elif ls.msgFromCar == 'util':
                print('ls.msgFromCar = ' + ls.msgFromCar)
                ls.msgFromCar=''
                sleep(1)
                sender.publish("ev3/to/car", 'ok')
                mp.go(0)
                mp.go(1, 'input')
                whereToGoArray=tools.find_sklad_util()
                if whereToGoArray[0]==0:
                    #  поехали в sklad1
                    move_oracul('sklad1')
                    move_Pi('adjust')
                if whereToGoArray[0] == 1:
                       #  поехали в sklad1
                    move_oracul('sklad2')
                    move_Pi('adjust')
                if whereToGoArray[0] == 2:
                   #  поехали в sklad1
                    move_oracul('sklad3')
                    move_Pi('adjust')
                mp.go(whereToGoArray[1]+1,"get")
                mp.move_forward()
                mp.go(whereToGoArray[1]+1,"up")
                mp.move_backward()
                move_oracul('util')      #приехали в util
                mp.go(0)
                mp.go(1, 'util')
                time.sleep(2)
                mp.move_forward()
                time.sleep(0.5)
                mp.go(2, "drop")
                time.sleep(0.5)
                mp.move_backward()

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
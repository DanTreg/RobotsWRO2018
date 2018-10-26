from ev3dev.ev3 import *
import time
import math
from time import sleep

ts1 = TouchSensor('in1')
assert ts1.connected; "Connect a touch sensor to sensor port 1"
ts2 = TouchSensor('in2')
assert ts2.connected; "Connect a touch sensor to sensor port 1"

mD = LargeMotor('outD')
mA = MediumMotor('outA')
mB = MediumMotor('outB')
mC = MediumMotor('outC')

p1 = 0
v1 = -250
p2 = 300
v2 = 0
p3 = 1750
v3 = 1430
p4 = -1500
v4 = -1800
t1 = 350
t2 = -350
t5=400
g=0
time=1350
time2=1800
time3=3300
time4=2100
timein=1600
power=50
alfa=90
alfa_r=math.radians(alfa)   #перевод угла в радианы
print(alfa_r)
y=round(math.cos(alfa_r),2)
x=round(math.sin(alfa_r),2)
print(x)
print(y)
a=[[0.58,-0.33,0.33],[-0.58,-0.33,0.33],[0,0.67,0.33]]
n=[-x,y,0]
c=[0,0,0]
c[0]=round((a[0][0]*n[0]+a[0][1]*n[1]+a[0][2]*n[2])*power,2)
c[1]=round((a[1][0]*n[0]+a[1][1]*n[1]+a[1][2]*n[2])*power,2)
c[2]=round((a[2][0]*n[0]+a[2][1]*n[1]+a[2][2]*n[2])*power,2)
print(c)
c[0]=c[0]*10
c[1]=c[1]*10
c[2]=c[2]*10

def move_forwardin():
    mA.run_timed(time_sp=timein, speed_sp=c[0])
    mB.run_timed(time_sp=timein, speed_sp=c[1])
    mC.run_timed(time_sp=timein, speed_sp=c[2])
    mA.wait_while('running')
def move_forwardoutt():
    mA.run_timed(time_sp=time4, speed_sp=c[0])
    mB.run_timed(time_sp=time4, speed_sp=c[1])
    mC.run_timed(time_sp=time4, speed_sp=c[2])
    mA.wait_while('running')
def move_forwardout():
    mA.run_timed(time_sp=time2, speed_sp=c[0])
    mB.run_timed(time_sp=time2, speed_sp=c[1])
    mC.run_timed(time_sp=time2, speed_sp=c[2])
    mA.wait_while('running')
    #sleep(1)
def move_forward():
    mA.run_timed(time_sp=time, speed_sp=c[0])
    mB.run_timed(time_sp=time, speed_sp=c[1])
    mC.run_timed(time_sp=time, speed_sp=c[2])
    mA.wait_while('running')
    #sleep(1)

def move_backward():
    mA.run_timed(time_sp=time+300, speed_sp=-c[0])
    mB.run_timed(time_sp=time+300, speed_sp=-c[1])
    mC.run_timed(time_sp=time+300, speed_sp=-c[2])
    mA.wait_while('running')
    #sleep(1)
def move_backwardout():
    mA.run_timed(time_sp=time3, speed_sp=-c[0])
    mB.run_timed(time_sp=time3, speed_sp=-c[1])
    mC.run_timed(time_sp=time3, speed_sp=-c[2])
    mA.wait_while('running')
    #sleep(1)

def go(flor, todo=''):
    global g
    if flor==0:
        while ts2.value() != 1:
            mD.run_forever(speed_sp=-500)

        mD.stop(stop_action="hold")
        g=0
    if flor == 1 and todo == 'get':
        while ts2.value() != 1:
            mD.run_forever(speed_sp=-500)

        mD.stop(stop_action="hold")
        mD.run_to_rel_pos(position_sp=v2, speed_sp=500, stop_action="hold")
        sleep(1)
        g=0
    elif flor == 1 and todo == 'put':
        '''
        while ts2.value() != 1:
            mD.run_forever(speed_sp=-500)

        mD.stop(stop_action="hold")
        '''
        mD.run_to_rel_pos(position_sp=p2-g, speed_sp=500, stop_action="hold")
        sleep(1)
        g=p2
    elif flor == 2 and todo == 'get':
        '''
        while ts2.value() != 1:
            mD.run_forever(speed_sp=-500)

        mD.stop(stop_action="hold")
        sleep(1)
        '''
        mD.run_to_rel_pos(position_sp=v3-g, speed_sp=500, stop_action="hold")
        sleep(3)
        g=v3
    elif flor == 2 and todo == 'put':
        '''
        while ts2.value() != 1:
            mD.run_forever(speed_sp=-500)

        mD.stop(stop_action="hold")
        '''
        mD.run_to_rel_pos(position_sp=p3-g, speed_sp=500, stop_action="hold")
        #print("go(3,put)")
        sleep(3.5)
        g=p3


    elif flor == 3 and todo == 'get':
        '''
        while ts1.value() != 1:
            mD.run_forever(speed_sp=500)

        mD.stop(stop_action="hold")
        '''
        mD.run_to_rel_pos(position_sp=2800-g, speed_sp=500, stop_action="hold")
        sleep(1)
        g=2800
    elif flor == 3 and todo == 'put':
        while ts1.value() != 1:
            mD.run_forever(speed_sp=500)

        mD.stop(stop_action="hold")
        mD.run_to_rel_pos(position_sp=p1, speed_sp=500, stop_action="hold")
        sleep(1)
        g=3050
    elif flor == 1 and todo == 'input':
        """        while ts1.value() != 1:
            print(ts1.value())
            mD.run_forever(speed_sp=500)"""


        #mD.stop(stop_action="hold")
        mD.run_to_rel_pos(position_sp=800-g, speed_sp=500, stop_action="hold")
        sleep(1)
        g=800
    elif flor == 1 and todo == 'output':
        """        while ts1.value() != 1:
            print(ts1.value())
            mD.run_forever(speed_sp=500)"""


        #mD.stop(stop_action="hold")
        mD.run_to_rel_pos(position_sp=1300-g, speed_sp=500, stop_action="hold")
        sleep(1)
        g=1300
    elif flor == 1 and todo == 'util':
        """        while ts1.value() != 1:
            print(ts1.value())
            mD.run_forever(speed_sp=500)"""


        #mD.stop(stop_action="hold")
        mD.run_to_rel_pos(position_sp=1500-g, speed_sp=500, stop_action="hold")
        sleep(1)
        g=1500
    elif todo == 'utilint':
        """        while ts1.value() != 1:
            print(ts1.value())
            mD.run_forever(speed_sp=500)"""

        # mD.stop(stop_action="hold")
        mD.run_to_rel_pos(position_sp=1100-g, speed_sp=500, stop_action="hold")
        g=1100
    elif flor!=1 and todo == 'drop':
        mD.run_to_rel_pos(position_sp=t2, speed_sp=500, stop_action="hold")
        sleep(1)
        g=g+t2
    elif flor!=3 and todo == 'up':
        mD.run_to_rel_pos(position_sp=t1, speed_sp=500, stop_action="hold")
        sleep(1)
        g=g+t1
    elif todo == 'upp':
        mD.run_to_rel_pos(position_sp=150, speed_sp=500, stop_action="hold")
        g=g+150

    elif flor==3 and todo == 'up':
        while ts1.value() != 1:
            mD.run_forever(speed_sp=500)

        mD.stop(stop_action="hold")
        sleep(1)
        g=3050
    elif flor==1 and todo == 'drop':
        while ts2.value() != 1:
            mD.run_forever(speed_sp=-500)

        mD.stop(stop_action="hold")
        sleep(1)
        g=0
    elif flor==1 and todo == 'droputil':
        mD.run_to_rel_pos(position_sp=-300, speed_sp=500, stop_action="hold")
        g=g-300
    elif flor==1 and todo == 'dropout':
        mD.run_to_rel_pos(position_sp=-400, speed_sp=500, stop_action="hold")
        g=g-400
    elif todo == 'dropint':
        mD.run_to_rel_pos(position_sp=-550, speed_sp=500, stop_action="hold")
        g=g-550
    elif todo == 'init':
        mD.run_to_rel_pos(position_sp=100, speed_sp=500, stop_action="hold")
        g=g+100
    elif todo == '350':
        mD.run_to_rel_pos(position_sp=t1-g, speed_sp=500, stop_action="hold")
        g=t1
'''
go(2, "get")
move_forwardoutt()
go(2, "upp")
move_backwardout()

go(0)
go(1, 'util')
sleep(2)
move_forwardoutt()
sleep(1)
go(1, "droputil")
sleep(1.2)
move_backward()

go(0)
go(1,'utilint')
sleep(2)
move_backward()
sleep(2)
go(2,'up')
sleep(2)
go(2,'drop')
sleep(2)
go(1,'dropint')

go(0,'init')
sleep(1)
go(1, 'utilint')
sleep(1.5)
move_forwardoutt()
sleep(1)
go(2, "up")
sleep(1)
move_backward()

sleep(1)
go(2,'get')
sleep(1)
go(0,'init')
sleep(1)
go(2,'put')
'''
import cv2
import RPi.GPIO as gpio
from datetime import datetime
import requests
import time
import zbarlight
import requests
#from pyzbar.pyzbar import decode
from PIL import Image
import PIL
import json
import os
import numpy as np
import paho.mqtt.client as mqtt
from threading import Thread
im_center = (320,240)
sq_center = (0,0)

adjust_conf = 0
go_x_conf = 0

product = None
image = None
camera = cv2.VideoCapture(0)
x,y,w,h = None,None,None,None

start = 'start'

cv2.namedWindow('Original')
cv2.moveWindow('Original', 500,100)

msgFromJohn = ""
class ListenJohn(Thread):
    
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
        listener.subscribe("ev3/to/pi")
        print("I am listening to ev3")

    def on_message(self, client, userdata, msg):
        global msgFromJohn
        msgFromJohn = msg.payload.decode()
        print("ev3 says: " + msgFromJohn)

        
listener = mqtt.Client()
sender = mqtt.Client()




my_thread = ListenJohn("Listen to John")

my_thread.start()
sender.connect("192.168.0.110",1883,1000)
def check_box():
    global x
    global y
    global w
    global sq_center
    global image
    global camera
    ret, image = camera.read()

    arrMinW = np.array([25, 106, 0])
    arrMaxW = np.array([40, 255, 255])

    frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    thresh = cv2.inRange(frame_to_thresh, (arrMinW), (arrMaxW))
    
    
    
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if len(cnts) > 0:
        
        c = max(cnts, key=cv2.contourArea)
        M = cv2.moments(c)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        print(x, w, y, h)
        #((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print(center)
        sq_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return True
            
def go_x_1():
    global x
    global y
    global w
    global h
    global adjust_conf
    global go_x_conf
    global image
    best = 170
    go_x_conf = 0
    while True:
        dlin = (abs(best - w) >= 5)
        check_box()
        cv2.imshow("Original", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        if w - best >= 9:
            dlina_h = w - best * 2
            print('GO BACKWARD...' + str(dlina_h))
            sender.publish('pi/to/ev3', 'a270' + 'd' + str(dlina_h))
            continue
        else:
            if dlin == False:
                go_x_conf = 1
                print("X OK")
                break
            else:
                dlin_f = abs(best - w) * 2
                print("MOVE FORWARD " + str(dlin_f))
                sender.publish("pi/to/ev3", "a90" + "d" + str(dlin_f))
                continue
        
def check_end():
    global sq_center
    global im_center
    global sender
    global go_x_conf
    global adjust_conf
    
    if go_x_conf == 1 and adjust_conf == 1:
        sender.publish('pi/to/ev3', 'a0' + 'd0')
        print('done')
        return True
    
    else:
        return True



def go_x():
    global x
    global y
    global w
    global h
    global adjust_conf
    global go_x_conf
    global image
    best = 200
    go_x_conf = 0
    while True:
        dlin = (abs(best - w) >= 5)
        check_box()
        cv2.imshow("Original", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        if w - best >= 9:
            dlina_h = w - best * 2
            print('GO BACKWARD...' + str(dlina_h))
            sender.publish('pi/to/ev3', 'a270' + 'd' + str(dlina_h))
            continue
        else:
            if dlin == False:
                go_x_conf = 1
                print("X OK")
                break
            else:
                dlin_f = abs(best - w) * 2
                print("MOVE FORWARD " + str(dlin_f))
                sender.publish("pi/to/ev3", "a90" + "d" + str(dlin_f))
                continue
def qrRead():
    global camera
    global sender
    global product
    ret,frame = camera.read()
    
    
    url = 'http://robots.therdteam.com/api/v2/products/createfromapi'
    
    headers2 = {'content-type': 'application/json'}
    
    
    cv2.imwrite('foo.jpg',frame)
    
    print("Scanning image..")
    f = open('foo.jpg','rb')
    
    #ar = frame.array
    #qr = PIL.Image.open(f);
    qr = PIL.Image.open(f)
    qr.load()
        #data = decode(qr)
        
    codes = zbarlight.scan_codes("qrcode",qr)
    if(codes==None):
                #os.remove('qr_codes/qr_0.jpg')
            print('No QR code found')
            return ''
    else:
            print('QR code(s):')
            print (codes)
            print (str(codes[0])[2])
                #if codes[0] == '1':
            if str(codes[0])[2] == 'e':
                return ''
            else:
                print(str(codes[0].decode()))
                data_r = str(codes[0].decode())
                print('hochu post')             
                print('post bil')
                    #print(str(r.content))
                
                product = data_r
                return data_r
def adjust():
    
    global sq_center
    global sender
    global im_center
    global adjust_conf
    global go_x_conf
    global image
    adjust_conf = 0
    while True:
        check_box()
        cv2.imshow("Original", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
              break
        if abs(sq_center[0] - im_center[0]) <= 5:
            adjust_conf = 1
            print('POS OK')
            break
        else:
            print(sq_center)
            print(im_center)
            if (sq_center[0] < im_center[0]) :
                print('q')
                dlin = abs(im_center[0] - sq_center[0])
                dlin_h = abs(sq_center[0] - im_center[0])
                
                print("ADJUST LEFT... " + str(dlin))
                sender.publish("pi/to/ev3", "a180" + "d" + str(dlin))
                continue
            
            else:
                print('r')
                dlin = abs(sq_center[0] - im_center[0])
                print("ADJUST RIGHT..." + str(dlin))
                sender.publish("pi/to/ev3", "a0" + "d" + str(dlin))
                continue
        


def readGAZ():
    global product
    global sender
    gpio.setmode(gpio.BCM)
    gpio.setup(14, gpio.IN)
    i = 0
    while i <= 1000000:
        data = False
        input_value = gpio.input(14)
        i+=1
        if (i==1000000):
            print('vishli: ',data)
            sender.publish('pi/to/ev3', str(product) +' '+ 'True')
            return str(data)
        if input_value == False:
            data = True
            print('The button has been pressed...')
            time.sleep(7)
            sender.publish('pi/to/ev3', str(product) +' '+ 'False')
            return str(data)
            
            break
        
            while input_value == False:
                input_value = gpio.input(14)
         
def main():
    global camera
    global msgFromJohn
    global go_x_conf
    global adjust_conf
    try:
        while True:
            
            ret, img = camera.read()
            cv2.circle(img,(260,240), 10, (0,255,255), -1)
            cv2.imshow("Original", img)
            
        
        
            if msgFromJohn != '':
                
                if msgFromJohn == 'adjust':
                    msgFromJohn = ''
                    check_box()
                    adjust()
                    go_x_1()
                    adjust()
                    print('!!!')
                    sender.publish('pi/to/ev3','a0d0')
                    
                    
                if msgFromJohn == 'adjust1':
                    msgFromJohn = ''
                    check_box()
                    adjust()
                    go_x()
                    adjust()
                    print('!!!')
                    sender.publish('pi/to/ev3','a0d0')
                
                if msgFromJohn == 'readQR':
                    time.sleep(2)
                    qrRead()
                    msgFromJohn = ''
                
                if msgFromJohn == 'readGAZ':
                    readGAZ()
                    msgFromJohn = ''
                    
            adjust_conf = 0
            go_x_conf = 0
            if cv2.waitKey(10) & 0xFF == ord('q'):
              break
    finally:
        listener.disconnect()
        self = False

if start == 'start':
    main()
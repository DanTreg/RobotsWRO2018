import cv2
import numpy as np
import math
import time
from datetime import datetime
import paho.mqtt.client as mqtt
from threading import Thread, Lock


class ListenEv4(Thread):

    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        pc.connect("192.168.1.110", 1883, 60)
        pc.on_connect = self.on_connect
        pc.on_message = self.on_message
        print("client is created")

    def run(self):
        print("thread start")
        pc.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        pc.subscribe("ev4/to/pc")
        print("I am listening to ev4")

    def on_message(self, client, userdata, msg):
        global msgFromEv4
        msgFromEv4 = msg.payload.decode()
        print("ev4 says: " + msgFromEv4)

class ListenEv3(Thread):

    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        listener.connect("192.168.1.110", 1883, 60)
        listener.on_connect = self.on_connect
        listener.on_message = self.on_message
        print("client is created")

    def run(self):
        print("thread start")
        listener.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        listener.subscribe("ev3/to/pc")
        print("I am listening to ev3")

    def on_message(self, client, userdata, msg):
        global msgFromEv3
        msgFromEv3 = msg.payload.decode()
        print("ev3 says: " + msgFromEv3)




class cap_circles(Thread):
    def __init__(self):
        super(cap_circles, self).__init__()
        self.const = True
        self.camera = cv2.VideoCapture(0)

    def run(self):
        print("thread start")
        while (self.const):
            global cenY
            global cenB
            global cenR
            global cenG
            global cenX1
            global cenY1
            global cenX2
            global cenY2
            global circle_radius
            global rotate_flag_robot1
            global rotate_flag_robot2
            global x_flag_robot2
            global x_flag_robot1
            global endPoint
            global endPoint1
            global flag_obezd
            #time_start = datetime.now()
            ret, image = self.camera.read()
            kk = 0
            while kk < 1:
                ret, image = self.camera.read()
                kk += 1
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            arrMinB = np.array([53, 181, 47])
            arrMaxB = np.array([136, 255, 255])

            arrMinY = np.array([15, 44, 240])
            arrMaxY = np.array([65, 199, 255])

            arrMinR = np.array([119, 136, 104])
            arrMaxR = np.array([255, 255, 255])

            arrMinG = np.array([33, 89, 76])
            arrMaxG = np.array([61, 165, 255])

            for number in [0, 1, 2, 3]:

                if number == 0:
                    thresh = cv2.inRange(frame_to_thresh, (arrMinY), (arrMaxY))
                if number == 1:
                    thresh = cv2.inRange(frame_to_thresh, (arrMinB), (arrMaxB))
                if number == 2:
                    thresh = cv2.inRange(frame_to_thresh, (arrMinR), (arrMaxR))
                if number == 3:
                    thresh = cv2.inRange(frame_to_thresh, (arrMinG), (arrMaxG))

                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None
                # only proceed if at least one contour was found
                if len(cnts) > 0:
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]),
                              int(M["m01"] / M["m00"]))  # Подобранные коэффиценты для нахождения центра контур

                    if number == 0:
                        cenY = center
                    if number == 1:
                        cenB = center
                    if number == 2:
                        cenR = center
                    if number == 3:
                        cenG = center

            cenY2 = round((cenY[1] + cenB[1]) / 2)
            cenX2 = round((cenY[0] + cenB[0]) / 2)
            cenY1 = round((cenR[1] + cenG[1]) / 2)
            cenX1 = round((cenR[0] + cenG[0]) / 2)
            cenYradius = 130
            cenRradius = 130
            cv2.circle(image, (480, 90), 5, (0, 255, 255), -1)
            cv2.circle(image, (cenR[0], cenR[1]), 10, (0, 255, 255), -1)
            cv2.circle(image, (cenG[0], cenG[1]), 10, (0, 255, 255), -1)
            cv2.circle(image, (cenY[0], cenY[1]), 10, (0, 255, 255), -1)
            cv2.circle(image, (cenB[0], cenB[1]), 10, (0, 255, 255), -1)
            cv2.circle(image, (cenX1, cenY1), cenRradius, (0, 255, 255), 1)
            cv2.circle(image, (cenX2, cenY2), cenYradius, (0, 255, 255), 1)
            cv2.line(image, (560, 420), (560, 50), (0,255,255), 10)
            cv2.line(image, (60, 420), (60, 50), (0,255,255), 10)
            cv2.line(image, (560, 50), (60, 50), (0,255,255), 10)
            cv2.line(image, (60, 420), (560, 420), (0,255,255), 10)


            
            cv2.imshow("Original", image)


            sum_radius = cenYradius + cenRradius

            #S = abs(abs(math.sqrt(abs(cenX1 - cenX2))) + (abs(cenY1 - cenY2))
            S = math.sqrt(pow(cenX2 - cenX1, 2) + pow(cenY2 - cenY1, 2))
            if sum_radius > S:
                rotate_flag_robot1 = 1
                rotate_flag_robot2 = 1
                
            img = image.copy()
            grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            retval, threshold = cv2.threshold(grayscaled, 255, 255, cv2.THRESH_BINARY)
            cv2.line(threshold, (cenX1, cenY1), (endPoint[0], endPoint[1]), (255, 255, 255), 35)
            cv2.line(threshold, (cenX2, cenY2), (endPoint1[0], endPoint1[1]), (255, 255, 255), 35)
            cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) == 2:
                if x_flag_robot2 == 1:
                    x_flag_robot2 = 0
                else:
                    pass
                #print('gotcha')
            if len(cnts) == 1:
                if x_flag_robot2 == 0:
                    x_flag_robot2 = 1
                else:
                    pass
                #print('gotcha1')

            cv2.imshow("original", threshold)
                #time_end = datetime.now()
                #print('centers:', cenR, cenG)
                #print(time_end-time_start)
            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

            img_obezd = image.copy()
            grayscaled = cv2.cvtColor(img_obezd, cv2.COLOR_BGR2GRAY)
            retval, threshold = cv2.threshold(grayscaled, 255, 255, cv2.THRESH_BINARY)
            cv2.circle(threshold, (cenX1, cenY1), circle_radius, (255, 255, 255), -1)
            cv2.circle(threshold, (cenX2, cenY2), circle_radius, (255, 255, 255), -1)
            cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            
            
            if len(cnts) == 2:
                if flag_obezd == 1:
                    flag_obezd = 0
                else:
                    pass
                if x_flag_robot1 == 1:
                    x_flag_robot1 = 0
                else:
                    pass

            if len(cnts) == 1:
                if flag_obezd == 0:
                    flag_obezd = 1
                else:
                    pass
                if x_flag_robot1 == 0:
                    x_flag_robot1 = 1
                else:
                    pass 
                
            cv2.putText(threshold,'circle radius:' + str(circle_radius), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 255, 255),1)
            cv2.imshow("original1", threshold)
                #time_end = datetime.now()
                #print('centers:', cenR, cenG)
                #print(time_end-time_start)
            if cv2.waitKey(1) & 0xFF is ord('q'):
                break

    def stop(self):
        self.const = False


class navigation_ev3(Thread):

    def __init__(self):
        global senderEv3
        super(navigation_ev3, self).__init__()
        senderEv3.connect("192.168.1.110", 1883, 1000)
        self.constEv3 = True

    def run(self):
        self.main()

    def go_x(self):  # Надо ли двигаться по х
        global cenR
        global cenG
        global endPoint
        global nameEndPoint
        global senderEv3
        global x_flag_robot1
        cenY = cenR[1] - (cenR[1] - cenG[1])
        cenX = cenR[0] - (cenR[0] - cenG[0])
        catX = abs(endPoint[0] - cenX)
        catY = abs(endPoint[1] - cenY)
        gipX = round(math.sqrt(pow(catX, 2) + pow(catY, 2)))
        angle = round(math.degrees(math.acos(catY / gipX)))

        if abs(cenR[0] - endPoint[0]) > 3:
            if nameEndPoint == "zona1":
                if x_flag_robot1 == 1:
                    senderEv4.publish("pc/to/ev3", 'a1000d1000')
                    print('STOOOOOOOP!!!')
                    return False
                else:
                    if cenR[0] < endPoint[0] and cenR[1] >= endPoint[1]:
                        angle_f = (90 - angle) + 180
                        print("GO TO VECTOR1 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenR[0] < endPoint[0] and cenR[1] < endPoint[1]:
                        angle_f = 90 + angle
                        print("GO TO VECTOR2 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenR[0] >= endPoint[0] and cenR[1] < endPoint[1]:
                        angle_f = 90 - angle
                        print("GO TO VECTOR3 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenR[0] >= endPoint[0] and cenR[1] >= endPoint[1]:
                        angle_f = angle + 270
                        print("GO TO VECTOR4 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
            else:
                if x_flag_robot1 == 1:
                    senderEv4.publish("pc/to/ev3", 'a1000d1000')
                    print('STOOOOOOOP!!!')
                    return False
                else:
                    if cenR[0] < endPoint[0] and cenR[1] >= endPoint[1]:
                        angle_f = 90 - angle
                        print("GO TO VECTOR1 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenR[0] < endPoint[0] and cenR[1] < endPoint[1]:
                        angle_f = angle + 270
                        print("GO TO VECTOR2 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenR[0] >= endPoint[0] and cenR[1] < endPoint[1]:
                        angle_f = (90 - angle) + 180
                        print("GO TO VECTOR3 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenR[0] >= endPoint[0] and cenR[1] >= endPoint[1]:
                        angle_f = 90 + angle
                        print("GO TO VECTOR4 ", str(angle_f))
                        senderEv3.publish("pc/to/ev3", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False

        else:
            return True

    def check_position(self):  # Надо ли повернутся
        global cenR
        global cenG
        global cenY
        global cenB
        global endPoint
        global nameEndPoint
        global senderEv3
        global rotate_flag_robot1
        dxCen = abs(cenR[0] - cenG[0])
        if dxCen == 0:
            dxCen = 1
        dyCen = abs(cenR[1] - cenG[1])
        if dyCen == 0:
            dyCen = 1

        if (abs(cenR[0] - cenG[0]) <= 6 and cenR[1] < cenG[1] and nameEndPoint == "zona2") or (
                abs(cenR[0] - cenG[0]) <= 6 and cenR[1] > cenG[1] and nameEndPoint == "zona1"):
            print("POS OK")
            return True
        else:
            if nameEndPoint == "zona1":
                print(cenR[0], cenG[0], cenR[1], cenG[1])
                tang = (dyCen / dxCen)
                atang = math.degrees(math.atan(tang))
                print(nameEndPoint, "input", "123")

                if cenR[0] >= cenG[0] and cenR[1] >= cenG[1]:
                    angle = (90 - atang)

                    if rotate_flag_robot1 == 1 and angle >= 40:
                        rotate_flag_robot1 = 0
                        if cenR[0] < cenY[0]:
                            if cenR[1] < cenG[1]:
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'l' + 'd' + '0')
                                print("ROTATE LEFT")
                                return False
                            else:
                                print("ROTATE RIGHT to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE RIGHT to ", str(round(angle, 2)))
                        senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                        return False
                if cenR[0] >= cenG[0] and cenR[1] < cenG[1]:
                    angle = (atang + 90)
                    if rotate_flag_robot1 == 1 and angle >= 40:
                        rotate_flag_robot1 = 0
                        if cenR[0] < cenY[0]:
                            if cenR[1] < cenG[1]:
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'l' + 'd' + '0')
                                print("ROTATE LEFT")
                                return False
                            else:
                                print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                        senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                        return False
                if cenR[0] < cenG[0] and cenR[1] < cenG[1]:
                    angle = (atang + 90)
                    if rotate_flag_robot1 == 1 and angle >= 40:
                        rotate_flag_robot1 = 0
                        if cenR[0] > cenY[0]:
                            if cenR[1] < cenG[1]:
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                print("ROTATE RIGHT")
                                return False
                            else:
                                print("ROTATE LEFT to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE LEFT to ", str(round(angle, 2)))
                        senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                        return False
                if cenR[0] < cenG[0] and cenR[1] >= cenG[1]:
                    angle = (90 - atang)
                    if rotate_flag_robot1 == 1 and angle >= 40:
                        rotate_flag_robot1 = 0
                        if cenR[0] > cenY[0]:
                            if cenR[1] < cenG[1]:
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                print("ROTATE RIGHT")
                                return False
                            else:
                                print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT1 to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE LEFT1 to ", str(round(angle, 2)))
                        senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                        return False

            else:
                    tang = (dyCen / dxCen)
                    atang = math.degrees(math.atan(tang))
                    if cenR[0] >= cenG[0] and cenR[1] >= cenG[1]:
                        angle = atang + 90
                        if rotate_flag_robot1 == 1 and angle >= 40:
                            rotate_flag_robot1 = 0
                            if cenR[0] > cenY[0]:
                                if cenR[1] < cenG[1]:
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                    print("ROTATE RIGHT")
                                    return False
                                else:
                                    print("ROTATE LEFT to ", str(round(angle, 2)))
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                    return False
                            else:
                                print("ROTATE LEFT to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    if cenR[0] >= cenG[0] and cenR[1] < cenG[1]:
                        angle = 90 - atang
                        if rotate_flag_robot1 == 1 and angle >= 40:
                            rotate_flag_robot1 = 0
                            if cenR[0] > cenY[0]:
                                if cenR[1] < cenG[1]:
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                    print("ROTATE RIGHT")
                                    return False
                                else:
                                    print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                    return False
                            else:
                                print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT1 to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    if cenR[0] < cenG[0] and cenR[1] < cenG[1]:
                        angle = 90 - atang
                        if rotate_flag_robot1 == 1 and angle >= 40:
                            rotate_flag_robot1 = 0
                            if cenR[0] < cenY[0]:
                                if cenR[1] < cenG[1]:
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'l' + 'd' + '0')
                                    print("ROTATE LEFT")
                                    return False
                                else:
                                    print("ROTATE RIGHT to ", str(round(angle, 2)))
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                    return False
                            else:
                                print("ROTATE RIGHT to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
                    if cenR[0] < cenG[0] and cenR[1] >= cenG[1]:
                        angle = atang + 90
                        if rotate_flag_robot1 == 1 and angle >= 40:
                            rotate_flag_robot1 = 0
                            if cenR[0] < cenY[0]:
                                if cenR[1] < cenG[1]:
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(360 - angle, 2)) + 'l' + 'd' + '0')
                                    print("ROTATE LEFT")
                                    return False
                                else:
                                    print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                    senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                    return False
                            else:

                                print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                            senderEv3.publish("pc/to/ev3", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
            nameEndPoint == ''

    def check_on_endPoint(self):  # На месте ли мы
        global cenR
        global cenG
        global endPoint
        global senderEv3
        global nameEndPoint
        if abs(cenR[0] - endPoint[0]) <= 5:
            senderEv3.publish("pc/to/ev3", "a0d0")
            self.check_position()
            print("ON END POINT OK")
            return True
        else:
            return True

    def main(self):
        global senderEv3
        global endPoint
        global nameEndPoint
        global msgFromEv3
        global cenG
        global cenR
        global circle_radius
        while (self.constEv3):
            while (self.constEv3):
                self.check_interception()
                time.sleep(1)
                if msgFromEv3 != '':
                    #print('in the loop')
                    if msgFromEv3 == 'sklad1':
                        msgFromEv3 = ''
                        endPoint = sklad1
                        nameEndPoint = 'zona2'
                    if msgFromEv3 == 'sklad2':
                        msgFromEv3 = ''
                        endPoint = sklad2
                        nameEndPoint = 'zona2'
                    if msgFromEv3 == 'sklad3':
                        msgFromEv3 = ''
                        endPoint = sklad3
                        nameEndPoint = 'zona2'
                    if msgFromEv3 == 'ok':
                        print('got ok')
                        msgFromEv3 = ''
                        continue
                    if msgFromEv3 == 'input':
                        msgFromEv3 = ''
                        endPoint = endInput
                        nameEndPoint = 'zona1'
                    if msgFromEv3 == 'output':
                        msgFromEv3 = ''
                        endPoint = endOutput
                        nameEndPoint = 'zona1'
                    if msgFromEv3 == 'util':
                        msgFromEv3 = ''
                        endPoint = endUtill
                        nameEndPoint = 'zona1'
                    if msgFromEv3 == 'test':
                        msgFromEv3 = ''
                        while True:
                            if len(cenG) == 2 and len(cenR) == 2:
                                senderEv3.publish("pc/to/ev3", 'ok')
                                break
                            else:
                                pass

                        continue

                    print("got message, go process frame")

                    break
                # time.sleep(2)
            circle_radius = 120
            if (self.check_position()):
                if (self.go_x()):
                    if (self.check_on_endPoint()):
                        print(" !!! ")

    def check_interception(self):
        global cenX2
        global cenY2
        global endUtill
        global circle_radius
        if cenX2 != None and cenY2 != None:

            length = math.sqrt(pow(cenX2 - endUtill[0], 2) + pow(cenY2 - endUtill[1], 2))
            if circle_radius > length:
                circle_radius = 100
            else:
                circle_radius = 120




    def stop(self):
        self.constEv3 = False




class navigation_ev4(Thread):

    def __init__(self):
        global senderEv4
        super(navigation_ev4, self).__init__()
        senderEv4.connect("192.168.1.110", 1883, 1000)
        self.constEv4 = True


    def run(self):
        self.main_1()

    def go_x_1(self):  # Надо ли двигаться по х
        global cenY
        global cenB
        global endPoint1
        global nameEndPoint1
        global senderEv4
        global x_flag_robot2
        #print('kek')
        cenY1 = cenY[1] - (cenY[1] - cenB[1])
        cenX1 = cenY[0] - (cenY[0] - cenB[0])
        catX = abs(endPoint1[0] - cenX1)
        catY = abs(endPoint1[1] - cenY1)
        gipX = round(math.sqrt(pow(catX, 2) + pow(catY, 2)))
        angle = round(math.degrees(math.acos(catY / gipX)))

        if abs(cenY[0] - endPoint1[0]) > 3:
            if nameEndPoint1 == "zona1":
                if x_flag_robot2 == 1:
                    senderEv4.publish("pc/to/ev4", 'a1000d1000')
                    print('STOOOOOOOP!!!')
                    return False
                else:
                    if cenY[0] < endPoint1[0] and cenY[1] >= endPoint1[1]:
                        angle_f = (90 - angle) + 180
                        print("GO TO VECTOR1 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenY[0] < endPoint1[0] and cenY[1] < endPoint1[1]:
                        angle_f = 90 + angle
                        print("GO TO VECTOR2 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenY[0] >= endPoint1[0] and cenY[1] < endPoint1[1]:
                        angle_f = 90 - angle
                        print("GO TO VECTOR3 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenY[0] >= endPoint1[0] and cenY[1] >= endPoint1[1]:
                        angle_f = angle + 270
                        print("GO TO VECTOR4 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
            else:
                if x_flag_robot2 == 1:
                    senderEv4.publish("pc/to/ev4", 'a1000d1000')
                    print('STOOOOOOOP!!!')
                    return False
                else:
                    if cenY[0] < endPoint1[0] and cenY[1] >= endPoint1[1]:
                        angle_f = 90 - angle
                        print("GO TO VECTOR1 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenY[0] < endPoint1[0] and cenY[1] < endPoint1[1]:
                        angle_f = angle + 270
                        print("GO TO VECTOR2 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenY[0] >= endPoint1[0] and cenY[1] < endPoint1[1]:
                        angle_f = (90 - angle) + 180
                        print("GO TO VECTOR3 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False
                    if cenY[0] >= endPoint1[0] and cenY[1] >= endPoint1[1]:
                        angle_f = 90 + angle
                        print("GO TO VECTOR4 ", str(angle_f))
                        senderEv4.publish("pc/to/ev4", 'a' + str(angle_f) + 'd' + str(abs(gipX)))
                        return False

        else:
            return True

    def check_position_1(self):  # Надо ли повернутся
        global cenY
        global cenB
        global cenR
        global cenG
        global endPoint1
        global nameEndPoint1
        global senderEv4
        global rotate_flag_robot2

        dxCen = abs(cenY[0] - cenB[0])
        if dxCen == 0:
            dxCen = 1
        dyCen = abs(cenY[1] - cenB[1])
        if dyCen == 0:
            dyCen = 1
        if (abs(cenY[0] - cenB[0]) <= 6 and cenY[1] < cenB[1] and nameEndPoint1 == "zona2") or (
                abs(cenY[0] - cenB[0]) <= 6 and cenY[1] > cenB[1] and nameEndPoint1 == "zona1"):
            print("POS OK")
            return True
        else:
            if nameEndPoint1 == "zona1":
                tang = (dyCen / dxCen)
                atang = math.degrees(math.atan(tang))
                #print(nameEndPoint1, "input", "123")

                if cenY[0] >= cenB[0] and cenY[1] >= cenB[1]:
                    angle = (90 - atang)
                    if rotate_flag_robot2 == 1 and angle >= 40:
                        rotate_flag_robot2 = 0
                        if cenY[0] < cenR[0]:
                            if cenY[1] < cenB[1]:
                                print("ROTATE LEFT to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'l' + 'd' + '0')
                                return False
                            else:
                                print("ROTATE RIGHT to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE RIGHT to ", str(round(angle, 2)))
                        senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                        return False
                if cenY[0] >= cenB[0] and cenY[1] < cenB[1]:
                    angle = (atang + 90)
                    if rotate_flag_robot2 == 1 and angle >= 40:
                        rotate_flag_robot2 = 0
                        if cenY[0] < cenR[0]:
                            if cenY[1] < cenB[1]:

                                print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'l' + 'd' + '0')
                                return False
                            else:
                                print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                        senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                        return False
                if cenY[0] < cenB[0] and cenY[1] < cenB[1]:
                    angle = (atang + 90)
                    if rotate_flag_robot2 == 1 and angle >= 40:
                        rotate_flag_robot2 = 0
                        if cenY[0] > cenR[0]:
                            if cenY[1] < cenB[1]:
                                print("ROTATE RIGHT to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                return False
                            else:
                                print("ROTATE LEFT to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE LEFT to ", str(round(angle, 2)))
                        senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                        return False
                if cenY[0] < cenB[0] and cenY[1] >= cenB[1]:
                    angle = (90 - atang)
                    if rotate_flag_robot2 == 1 and angle >= 40:
                        rotate_flag_robot2 = 0
                        if cenY[0] > cenR[0]:
                            if cenY[1] < cenB[1]:
                                print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                return False
                            else:
                                print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT1 to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    else:
                        print("ROTATE LEFT1 to ", str(round(angle, 2)))
                        senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                        return False


            else:
                    tang = (dyCen / dxCen)
                    atang = math.degrees(math.atan(tang))
                    if cenY[0] >= cenB[0] and cenY[1] >= cenB[1]:
                        angle = atang + 90
                        if rotate_flag_robot2 == 1 and angle >= 40:
                            rotate_flag_robot2 = 0
                            if cenY[0] > cenR[0]:
                                if cenY[1] < cenB[1]:
                                    print("ROTATE RIGHT to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                    return False
                                else:
                                    print("ROTATE LEFT to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                    return False
                            else:
                                print("ROTATE LEFT to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    if cenY[0] >= cenB[0] and cenY[1] < cenB[1]:
                        angle = 90 - atang
                        if rotate_flag_robot2 == 1 and angle >= 40:
                            rotate_flag_robot2 = 0
                            if cenY[0] > cenR[0]:
                                if cenY[1] < cenB[1]:
                                    print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'r' + 'd' + '0')
                                    return False
                                else:
                                    print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                    return False
                            else:
                                print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE LEFT1 to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'l' + 'd' + '0')
                            return False
                    if cenY[0] < cenB[0] and cenY[1] < cenB[1]:
                        angle = 90 - atang
                        if rotate_flag_robot2 == 1 and angle >= 40:
                            rotate_flag_robot2 = 0
                            if cenY[0] < cenR[0]:
                                if cenY[1] < cenB[1]:
                                    print("ROTATE LEFT to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'l' + 'd' + '0')
                                    return False
                                else:
                                    print("ROTATE RIGHT to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                    return False
                            else:
                                print("ROTATE RIGHT to ", str(round(angle,2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
                    if cenY[0] < cenB[0] and cenY[1] >= cenB[1]:
                        angle = atang + 90
                        if rotate_flag_robot2 == 1 and angle >= 40:
                            rotate_flag_robot2 = 0
                            if cenY[0] < cenR[0]:
                                if cenY[1] < cenB[1]:
                                    print("ROTATE LEFT1 to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(360 - angle, 2)) + 'L' + 'd' + '0')
                                    return False
                                else:
                                    print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                    senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                    return False
                            else:
                                print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                                senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                                return False
                        else:
                            print("ROTATE RIGHT1 to ", str(round(angle, 2)))
                            senderEv4.publish("pc/to/ev4", 'a' + str(round(angle, 2)) + 'r' + 'd' + '0')
                            return False
            nameEndPoint1 == ''

    def check_on_endPoint_1(self):  # На месте ли мы
        global cenY
        global cenB
        global endPoint1
        global senderEv4
        global nameEndPoint1
        if abs(cenY[0] - endPoint1[0]) <= 5:
            senderEv4.publish("pc/to/ev4", "a0d0")
            self.check_position_1()
            print("ON END POINT OK")
            return True
        else:
            return True

    def check_side(self, cenB, cenY, side_kskladu):
        if side_kskladu == False:
            if cenB[1] > cenY[1]:
                turn_side = 90
                return turn_side
            else:
                turn_side = 270
                return turn_side
        if side_kskladu == True:
            if cenB[1] > cenY[1]:
                turn_side = 270
                return turn_side
            else:
                turn_side = 90
                return turn_side

    def obezd(self):
        global cenX1
        global cenY1
        global cenX2
        global cenY2
        global cenB
        global cenY
        global circle_radius
        '''
        dist = abs(cenX1 - cenX2)
        dist_to_move_X = abs(dist - circle_radius * 2)
        dist_to_move_Y = circle_radius * 2
        '''
        d = 30

        if cenX2 >= 500 or cenX2 <= 60:
            print('kek1')
            if cenY2 <= 60 or cenY2 >= 500:
                if cenY2 <= 60:
                    side = self.check_side(cenB, cenY, True)
                else:
                    side = self.check_side(cenB, cenY, False)

                senderEv4.publish("pc/to/ev4", 'a' + str(side) + 'd' + str(d))
                return None
            else:
                side = self.check_side(cenB, cenY, False)
                senderEv4.publish("pc/to/ev4", 'a' + str(side) + 'd' + str(d))
                return None

        else:
            print('kek')
            side = self.check_direction()
            if side == 0:

                if cenX1 < cenX2:
                    senderEv4.publish("pc/to/ev4", 'a0' + 'd' + str(d))
                    print('turned to storage')
                    return None
                else:
                    senderEv4.publish("pc/to/ev4", 'a180' + 'd' + str(d))
                    print('turned to cars')
                    return None
            else:
                if cenX1 < cenX2:
                    senderEv4.publish("pc/to/ev4", 'a180' + 'd' + str(d))
                    print('turned to cars(180)')
                    return None
                else:
                    senderEv4.publish("pc/to/ev4", 'a0' + 'd' + str(d))
                    print('turned to storage(180)')
                    return None

    
    def check_direction(self):
        global cenB
        global cenY
        if cenY[1] < cenB[1]:
            side = 0
        if cenY[1] > cenB[1]:
             
            side = 180
        return side
        

    def main_1(self):
        global senderEv4
        global endPoint1
        global nameEndPoint1
        global msgFromEv4
        global cenB
        global cenY
        while (self.constEv4):
            while (self.constEv4):
                time.sleep(1)
                if msgFromEv4 != '':
                    #print('in the loop')

                    if msgFromEv4 == 'sklad1':
                        msgFromEv4 = ''
                        endPoint1 = sklad1
                        nameEndPoint1 = 'zona2'
                    if msgFromEv4 == 'sklad2':
                        msgFromEv4 = ''
                        endPoint1 = sklad2
                        nameEndPoint1 = 'zona2'
                    if msgFromEv4 == 'sklad3':
                        msgFromEv4 = ''
                        endPoint1 = sklad3
                        nameEndPoint1 = 'zona2'
                    if msgFromEv4 == 'ok':
                        print('got ok')
                        msgFromEv4 = ''
                        continue
                    if msgFromEv4 == 'input':
                        msgFromEv4 = ''
                        endPoint1 = endInput
                        nameEndPoint1 = 'zona1'
                    if msgFromEv4 == 'output':
                        msgFromEv4 = ''
                        endPoint1 = endOutput
                        nameEndPoint1 = 'zona1'
                    if msgFromEv4 == 'util':
                        msgFromEv4 = ''
                        endPoint1 = endUtill
                        nameEndPoint1 = 'zona1'
                    if msgFromEv4 == 'test':
                        msgFromEv4 = ''
                        while True:
                            if len(cenB) == 2 and len(cenY) == 2:
                                senderEv4.publish("pc/to/ev4", 'ok')
                                break
                            else:
                                pass

                        continue

                    print("got message, go process frame")

                    break
                # time.sleep(2)
                #print('kaef')
            if (self.check_position_1()):
                if flag_obezd == 1:
                        self.obezd()
                        msgFromEv4 = ''
                        continue
                #print('kaef1')
                if self.go_x_1():
                    if (self.check_on_endPoint_1()):
                        print(" !!! ")

    def stop(self):
        self.constEv4 = False


msgFromEv4 = ''
msgFromEv3 = ''

pc = mqtt.Client()
listener = mqtt.Client()
senderEv3 = mqtt.Client()
senderEv4 = mqtt.Client()


my_thread1 = ListenEv4("Listen to ev4")
my_thread = ListenEv3("Listen to Ev3")
grabber = cap_circles()
NavigationEv3 = navigation_ev3()
NavigationEv4 = navigation_ev4()

endPoint = (0, 0)
endPoint1 = (640, 0)
flag = 0 #флаг для избежания повторов
#END POINTS
#по инпуту
sklad1 = (160,100)
sklad2 = (320,100)
sklad3 = (470,100)
#по a_output


cenX1 = None
cenY1 = None
cenX2 = None
cenY2 = None


endInput = (70,350)
endOutput = (570,330)
endUtill = (310,350)

#NAMES END POINT
nameEndPoint = ''
nameEndPoint1 = ''

rotate_flag_robot1 = 0
rotate_flag_robot2 = 0


flag_obezd = 0
x_flag_robot2 = 0
x_flag_robot1 = 0

cenB = (0, 0)
cenY = (0, 0)
cenR = (0, 0)
cenG = (0, 0)
circle_radius = 120

try:
    grabber.start()
    my_thread.start()
    my_thread1.start()
    NavigationEv3.start()
    NavigationEv4.start()
    while True:
        pass
finally:
    grabber.stop()
    NavigationEv3.stop()
    listener.disconnect()
    pc.disconnect()
    NavigationEv4.stop()

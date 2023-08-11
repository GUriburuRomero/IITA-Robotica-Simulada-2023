from controller import Robot, Camera, Emitter, GPS
import cv2 as cv
import numpy as np
import struct

robot = Robot()

timeStep = int(robot.getBasicTimeStep())

wheel_left = robot.getDevice("wheel1 motor")  
wheel_right = robot.getDevice("wheel2 motor")

cam = robot.getDevice("camera1")
cam.enable(timeStep)

gps = robot.getDevice('gps')
gps.enable(timeStep)

emitter = robot.getDevice('emitter')

def delay(ms):
    initTime = robot.getTime()
    while robot.step(timeStep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def checkVic(img):
    img = np.frombuffer(img, np.uint8).reshape((cam.getHeight(), cam.getWidth(), 4)) 
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    img, thresh = cv.threshold(img, 80, 255, cv.THRESH_BINARY_INV) 
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        contArea = cv.contourArea(cnt)   
        ratio = w / h    
        print(contArea)
        if contArea > 180 and contArea < 1150 and ratio > 0.65 and ratio < 0.95: #200 900 300 1188
            return True
    return False

def report(victimType):
    wheel_left.setVelocity(0) 
    wheel_right.setVelocity(0)
    delay(1300)
    victimType = bytes(victimType, "utf-8")  
    posX = int(gps.getValues()[0] * 100)   
    posZ = int(gps.getValues()[2] * 100)
    message = struct.pack("i i c", posX, posZ, victimType)
    emitter.send(message)
    robot.step(timeStep)

while robot.step(timeStep) != -1:
    if checkVic(cam.getImage()):
        print("¡Detectada!")
        delay(1000)
        report('S')
        break

    else:
        print("Sin detectar")

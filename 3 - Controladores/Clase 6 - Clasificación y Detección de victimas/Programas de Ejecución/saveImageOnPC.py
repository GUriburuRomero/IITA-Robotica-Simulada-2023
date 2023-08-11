# Code for save an image on your PC from camera on Webots

from controller import Robot, Camera, DistanceSensor
import struct

from ultralytics import YOLO
import cv2 as cv
import numpy as np
import os

robot = Robot()
timeStep = int(robot.getBasicTimeStep())

estado = 'a'

sensorDistancia = robot.getDevice("d1")
sensorDistancia.enable(timeStep)


wheel_left = robot.getDevice('wheel2 motor')
wheel_right = robot.getDevice('wheel1 motor')

wheel_left.setPosition(float('inf'))
wheel_right.setPosition(float('inf'))

camara = robot.getDevice("camera1")
camara.enable(timeStep)

h = camara.getHeight()
w = camara.getWidth()

def w_velocity(vel):
    wheel_left.setVelocity(vel)
    wheel_right.setVelocity(vel)

while robot.step(timeStep) != -1:
    if estado == 'a':
        if sensorDistancia.getValue() <= 0.08:
            estado = "b"
        else:
            w_velocity(1.0)
    
    if estado == 'b':
        w_velocity(0.0)
        img = camara.getImage()
        img = np.array(np.frombuffer(img, np.uint8).reshape((h, w, 4)))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = cv.resize(img, (500, 500), interpolation=cv.INTER_LINEAR)
        #img = cv.colorChange(img, 'RGB')
        os.chdir(r"C:/Users/GERARDO URIBURU/Desktop") # Paste the path where u will save the image
        cv.imwrite("Imagen.png", img)
        break
    
    print(f'{sensorDistancia.getValue():.3}')
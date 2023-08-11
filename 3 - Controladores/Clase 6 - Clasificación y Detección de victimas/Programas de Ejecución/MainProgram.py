## Code for victim's classification using Yolo V8

from controller import Robot, Camera, DistanceSensor

from ultralytics import YOLO
import cv2 as cv
import numpy as np
import os

directorio = str(os.getcwd())

robot = Robot()
timeStep = int(robot.getBasicTimeStep())

the_dict = "a"
probs = "b"

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

def predict(img):
    global the_dict
    global probs
    img = cv.resize(img, (100, 100))
    model = YOLO("C:/Users/GERARDO URIBURU/Desktop/Principal/runs/classify/train2/weights/best.pt") # Paste the path here
    results = model(img)
    the_dict = results[0].names
    probs = results[0].probs.tolist()
    a = the_dict[np.argmax(probs)]
    print(a)

while robot.step(timeStep) != -1:
    if estado == 'a':
        if sensorDistancia.getValue() <= 0.07:
            estado = "b"
        else:
            w_velocity(1)
    
    if estado == "b":
        w_velocity(0)
        img = camara.getImage()
        img = np.array(np.frombuffer(img, np.uint8).reshape((h, w, 4)))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        #img = cv.colorChange(img, 'RGB')
        predict(img)
        break


    #print(sensorDistancia.getValue())
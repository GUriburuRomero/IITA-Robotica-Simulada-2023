from controller import Robot, Camera
import cv2
import numpy as np

robot = Robot()

timeStep = int(robot.getBasicTimeStep())

cam = robot.getDevice("camera1")
cam.enable(timeStep)

h = cam.getHeight()
w = cam.getWidth()

def ShapeDetection(img):

    img = cv2.resize(img, (100, 100))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
  
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
    i = 0

    for contour in contours:
    
        if i == 0:
            i = 1
            continue
    
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
    
        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
    
        # putting shape name at center of each shape
        if len(approx) == 4:
            return True
    return False

def prepareImage():
    imgC = cam.getImage()
    imgC = np.array(np.frombuffer(imgC, np.uint8).reshape((h, w, 4)))
    imgC = cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)
    imagenrgb = imgC
    return imgC


while robot.step(timeStep) != -1:
    if ShapeDetection(prepareImage()):
        print("Cartel detectado!")
    else:
        print("Sin detectar")


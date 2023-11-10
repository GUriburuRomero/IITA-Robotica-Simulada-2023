from controller import Robot, Camera, DistanceSensor
import cv2 as cv2
import numpy as np
import os

from PIL import Image

robot = Robot() 
timeStep = int(robot.getBasicTimeStep())

cam = robot.getDevice("camera1")
cam.enable(timeStep)

ds = robot.getDevice("distance sensor1")
ds.enable(timeStep)

h = cam.getHeight()
w = cam.getWidth()

# C:\Users\GERARDO URIBURU\Documents\IITA-Robotica-Simulada-2023\Simulador_Erebus\Erebus-v23_0_5\game\controllers\robot0Controller\personalImage.png

PATH_IMAGE = os.getcwd() + "\personalImage.png"

def ShapeDetection(img):
    ''' Shape detection on the camera image '''
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

def saveFinalImage(imgf):
    ''' Image save system on current directory '''
    imgf = np.array(np.frombuffer(imgf, np.uint8).reshape((h, w, 4)))
    imgf = cv2.cvtColor(imgf, cv2.COLOR_BGR2RGB)
    imgf = cv2.resize(imgf, (500, 500), interpolation=cv2.INTER_LINEAR)
    # imgf = cv2.colorChange(img, 'RGB')
    os.chdir(str(os.getcwd())) # Paste the path where u will save the image
    cv2.imwrite("personalImage.png", imgf)

def getImageCV(src):
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    print(src.shape)
    print("image array = \n", src[25][25])

def prepareImage():
    ''' Image fix for OpenCV Utilities'''
    imgC = cam.getImage()
    imgC = np.array(np.frombuffer(imgC, np.uint8).reshape((h, w, 4)))
    imgC = cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)
    imgC = cv2.resize(imgC, (500, 500), interpolation=cv2.INTER_LINEAR)
    return imgC

def get_image(image_path):
    ''' Image analysis pixel per pixel (colors) '''
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, "r")
    # image = image_path
    width, height = 500, 500
    pixel_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "L":
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = np.array(pixel_values).reshape((width, height, channels))
    return pixel_values

# Principal Loop
while robot.step(timeStep) != -1:
    img = cam.getImage()
    # print(ds.getValue())
    if ShapeDetection(prepareImage()) and ds.getValue() < 0.1 and ds.getValue() > 0.07:
        getImageCV(prepareImage())
        saveFinalImage(img)
        imageAnalysis = get_image(PATH_IMAGE)
        for i in range(100, 400, 10):
            for k in range(1, 500, 10):
                pixeles = imageAnalysis[i,k]
                print(pixeles)
        break

#Cargo controladores
from controller import Robot, Motor, GPS, DistanceSensor, Camera, Gyro, Emitter
import math
import numpy as np
import struct
import cv2 as cv2
import os
from PIL import Image


tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep())
angulo_actual = 0 
finalLetter = ""
PATH_IMAGE = os.getcwd() + "\personalImage.png"


#Motores:
wheel_left = robot.getDevice("wheel2 motor")    
wheel_right = robot.getDevice("wheel1 motor")

wheel_left.setPosition(float('inf')) 
wheel_right.setPosition(float('inf'))

leftEncoder = wheel_left.getPositionSensor()    
rightEncoder = wheel_right.getPositionSensor()

leftEncoder.enable(timeStep) 
rightEncoder.enable(timeStep)


#GPS:
gps = robot.getDevice("gps") 
gps.enable(timeStep) 


#Sensor de distancia:
distanceSensor1 = robot.getDevice("distance sensor1")
distanceSensor2 = robot.getDevice("distance sensor2")
distanceSensor3 = robot.getDevice("distance sensor3")
distanceSensor1.enable(timeStep)
distanceSensor2.enable(timeStep)
distanceSensor3.enable(timeStep)

#Sensor de color:
color = robot.getDevice("colour_sensor")
color.enable(timeStep)

#Giroscopo:
gyro = robot.getDevice('gyro')
gyro.enable(timeStep)

#Camaras:
Camera1 = robot.getDevice("camera1")
Camera2 = robot.getDevice("camera2")
Camera1.enable(timeStep)
Camera2.enable(timeStep)

hcamera1 = Camera1.getHeight()
wcamera1 = Camera1.getWidth()

hcamera2 = Camera2.getHeight()
wcamera2 = Camera2.getWidth()

#Emitter:
emitter = robot.getDevice('emitter')

#Funciones:
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

def saveFinalImage1(imgf):
    ''' Image save system on current directory '''
    imgf = np.array(np.frombuffer(imgf, np.uint8).reshape((hcamera1, wcamera1, 4)))
    imgf = cv2.cvtColor(imgf, cv2.COLOR_BGR2RGB)
    imgf = cv2.resize(imgf, (500, 500), interpolation=cv2.INTER_LINEAR)
    # imgf = cv2.colorChange(img, 'RGB')
    os.chdir(str(os.getcwd())) # Paste the path where u will save the image
    cv2.imwrite("personalImage.png", imgf)

def saveFinalImage2(imgf):
    ''' Image save system on current directory '''
    imgf = np.array(np.frombuffer(imgf, np.uint8).reshape((hcamera2, wcamera2, 4)))
    imgf = cv2.cvtColor(imgf, cv2.COLOR_BGR2RGB)
    imgf = cv2.resize(imgf, (500, 500), interpolation=cv2.INTER_LINEAR)
    # imgf = cv2.colorChange(img, 'RGB')
    os.chdir(str(os.getcwd())) # Paste the path where u will save the image
    cv2.imwrite("personalImage.png", imgf)

def classifyVictim1(img):
    '''Permite clasificar la imagen'''
    finalLetter = ""
    img = np.frombuffer(img, np.uint8).reshape((Camera1.getHeight(), Camera1.getWidth(), 4))
    img = cv2.resize(img, (100, 100)) # Redimensionamis la imagen
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convertimos la imagen a escala de grises para mejor detección
    thresh1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    conts, h = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(conts[0])

    letter = thresh1[y:y + h, x:x + w]
    letter = cv2.resize(letter, (100, 100), interpolation= cv2.INTER_AREA)

    areaWidth = 20
    areaHeight = 30

    areas = {
        "top": ((0, areaHeight),(50 - areaWidth // 2, 50 + areaWidth // 2)),
        "middle": ((50 - areaHeight // 2, 50 + areaHeight // 2), (50 - areaWidth // 2, 50 + areaWidth // 2)),
        "bottom": ((100 - areaHeight, 100), (50 - areaWidth // 2, 50 + areaWidth // 2 ))
        }

    images = {
        "top": letter[areas["top"][0][0]:areas["top"][0][1], areas["top"][1][0]:areas["top"][1][1]],
        "middle": letter[areas["middle"][0][0]:areas["middle"][0][1], areas["middle"][1][0]:areas["middle"][1][1]],
        "bottom": letter[areas["bottom"][0][0]:areas["bottom"][0][1], areas["bottom"][1][0]:areas["bottom"][1][1]]
        }

    counts = {}
    acceptanceThreshold = 50

    for key in images.keys():
        count = 0
        for row in images[key]:
            for pixel in row:
                if pixel == 255:
                    count += 1
        counts[key] = count > acceptanceThreshold

    letters = {
        "1":{'top': False, 'middle': True, 'bottom': False}, # H
        "2":{'top': True, 'middle': True, 'bottom': True},   # S
        "3":{'top': False, 'middle': False, 'bottom': True}  # U
        }

    for letterKey in letters.keys():
        if counts == letters[letterKey]:
            finalLetter = letterKey
            break
    
    if finalLetter == "1":
        report('H')
    elif finalLetter == "2":
        report('S')
    elif finalLetter == "3":
        report('U')


def classifyVictim2(img):
    '''Permite clasificar la imagen'''
    finalLetter = ""
    img = np.frombuffer(img, np.uint8).reshape((Camera2.getHeight(), Camera2.getWidth(), 4))
    img = cv2.resize(img, (100, 100)) # Redimensionamis la imagen
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convertimos la imagen a escala de grises para mejor detección
    thresh1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    conts, h = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(conts[0])

    letter = thresh1[y:y + h, x:x + w]
    letter = cv2.resize(letter, (100, 100), interpolation=cv2.INTER_AREA)

    areaWidth = 20
    areaHeight = 30

    areas = {
        "top": ((0, areaHeight),(50 - areaWidth // 2, 50 + areaWidth // 2)),
        "middle": ((50 - areaHeight // 2, 50 + areaHeight // 2), (50 - areaWidth // 2, 50 + areaWidth // 2)),
        "bottom": ((100 - areaHeight, 100), (50 - areaWidth // 2, 50 + areaWidth // 2 ))
        }

    images = {
        "top": letter[areas["top"][0][0]:areas["top"][0][1], areas["top"][1][0]:areas["top"][1][1]],
        "middle": letter[areas["middle"][0][0]:areas["middle"][0][1], areas["middle"][1][0]:areas["middle"][1][1]],
        "bottom": letter[areas["bottom"][0][0]:areas["bottom"][0][1], areas["bottom"][1][0]:areas["bottom"][1][1]]
        }

    counts = {}
    acceptanceThreshold = 50

    for key in images.keys():
        count = 0
        for row in images[key]:
            for pixel in row:
                if pixel == 255:
                    count += 1
        counts[key] = count > acceptanceThreshold

    letters = {
        "1":{'top': False, 'middle': True, 'bottom': False}, # H
        "2":{'top': True, 'middle': True, 'bottom': True},   # S
        "3":{'top': False, 'middle': False, 'bottom': True}  # U
        }

    for letterKey in letters.keys():
        if counts == letters[letterKey]:
            finalLetter = letterKey
            break
    
    if finalLetter == "1":
        report('H')
    elif finalLetter == "2":
        report('S')
    elif finalLetter == "3":
        report('U')

def delay(ms):
    initTime = robot.getTime()
    while robot.step(timeStep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def checkVic1(img):
    img = np.frombuffer(img, np.uint8).reshape((Camera1.getHeight(), Camera1.getWidth(), 4)) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    img, thresh = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY_INV) 
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        contArea = cv2.contourArea(cnt)   
        ratio = w / h    
        print(contArea)
        if contArea > 25 and contArea < 95 and ratio > 0.55 and ratio <= 0.95: #200 900 // 300 1188
            return True
    return False

def checkVic2(img):
    img = np.frombuffer(img, np.uint8).reshape((Camera2.getHeight(), Camera2.getWidth(), 4)) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    img, thresh = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY_INV) 
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        contArea = cv2.contourArea(cnt)   
        ratio = w / h    
        print(contArea)
        if contArea > 25 and contArea < 95 and ratio > 0.55 and ratio <= 0.95: #200 900 // 300 1188
            return True
    return False

def getImageCV(src):
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    print(src.shape)
    print("image array = \n", src[25][25])

def prepareImage1():
    ''' Image fix for OpenCV Utilities'''
    imgC = Camera1.getImage()
    imgC = np.array(np.frombuffer(imgC, np.uint8).reshape((hcamera1, wcamera1, 4)))
    imgC = cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)
    imgC = cv2.resize(imgC, (500, 500), interpolation=cv2.INTER_LINEAR)
    return imgC

def prepareImage2():
    ''' Image fix for OpenCV Utilities'''
    imgC = Camera2.getImage()
    imgC = np.array(np.frombuffer(imgC, np.uint8).reshape((hcamera2, wcamera2, 4)))
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

def analysisImage():
    contAzul = 0
    contCeleste = 0
    contNegro = 0
    contBlanco = 0
    imageAnalysis = get_image(PATH_IMAGE) ## Abro la imagen que guardamos anteriormente
    for i in range(90, 500, 10): ## Recorro los píxeles de la imagen
        for k in range(1, 500, 10):
            pixeles = imageAnalysis[i,k]
            if pixeles[0]<= 60 and pixeles[1]<= 60 and pixeles[2] < 60: ## Si los pixeles tienden a ser negros
                contNegro += 1 
            elif pixeles[0] >= 120 and pixeles[1] >= 120 and pixeles[2] >= 120: ## SI los pixeles tienden a ser blanco
                contBlanco += 1
            elif pixeles[0] <= 79 and pixeles[1] >= 0 and pixeles[2] <= 197: ## Si los pixeles tienden a ser azul oscuro
                contAzul += 1
            print(pixeles)

    print(f'Pixeles blancos: {contBlanco}, Pixeles Negros: {contNegro}, Pixeles azules: {contAzul}')

    if contNegro > contBlanco: ## Evalúo segun que características tiene cada cartel (cantidad de cada color)
        ## Clasifico (mejorar para reportar según letra de cartel)
        report("C")
        print("Es el cartel de color blanco y negro (corrosive)") ## Corrosive tiene mas negro que blanco, Poison tiene más blanco que negro, etc.
    elif contBlanco > contNegro:
        report("P")
        print("El cartel es poison")

    
def report(victimType):
    print(victimType)
    wheel_left.setVelocity(0) 
    wheel_right.setVelocity(0)
    delay(1300)
    victimType = bytes(victimType, "utf-8")  
    posX = int(gps.getValues()[0] * 100)   
    posZ = int(gps.getValues()[2] * 100)
    message = struct.pack("i i c", posX, posZ, victimType)
    emitter.send(message)
    robot.step(timeStep)

def w_velocity(vel):
    ''' Función para que el robot avance'''
    wheel_left.setVelocity(vel)
    wheel_right.setVelocity(vel)

def turn(vel):
    ''' Función para la rotación del robot'''
    wheel_left.setVelocity(vel)
    wheel_right.setVelocity(-vel)

def turn_gyro(angle, velTurn):
    ''' Función para rotar la cantidad de grados que indiquemos'''
    global angulo_actual
    tiempo_anterior = 0

    turn(velTurn)
    while ( abs(angle - angulo_actual) > 1):

        tiempo_actual = robot.getTime()
        tiempo_transcurrido = tiempo_actual - tiempo_anterior 

        radsIntimestep = abs(gyro.getValues()[1]) * tiempo_transcurrido
        degsIntimestep = radsIntimestep * 180 / math.pi 

        print(f"degs: {degsIntimestep:.3f}")
    
        angulo_actual += degsIntimestep
        angulo_actual = angulo_actual % 360

        if angulo_actual < 0:
            angulo_actual += 360

        tiempo_anterior = tiempo_actual
        robot.step(timeStep)

    print("Rotacion finalizada.")
    angulo_actual = 0
    w_velocity(0)
    return True

def colourDetector(r, g, b):
    ''' Función para detectar el color en tiempo real '''
    color = "s/n"
    if (180 <= r <= 202) and (150 <= g <= 170) and (80 <= b <= 97):
        color = "swamp"
        print("Se detecto un swamp")
    elif (100<= r <= 104) and (102 <= g <= 108) and (114 <= b <=118):
        color = "checkpoint"
        print("Se detecto un checkpoint")
    elif 30 <= (r and g and b) <= 38:
        color = "hole"
        print("Se detecto un hole")
    return color  

start = robot.getTime() 
robot.step(timeStep) 

sy = gps.getValues()[0]/tilesize 
sx = gps.getValues()[0]/tilesize 

state = "calibracion_inicial"
while robot.step(timeStep) != -1: 
    
    y = round(gps.getValues()[0]/tilesize - sy, 1) 
    x = round(gps.getValues()[2]/tilesize - sx, 1) 
    encoder_right_real = float(rightEncoder.getValue())
    encoder_left_real = float(leftEncoder.getValue())

    print("Left motor has spun " + str(leftEncoder.getValue()) + " radians")   
    print("Right motor has spun " + str(rightEncoder.getValue()) + " radians")

    print(f'x: {x}, y: {y}')

    distancia1 = distanceSensor1.getValue()
    print(f'La distancia1 o sensor de la derecha es de {distancia1:.3f} metros')

    distancia2 = distanceSensor2.getValue()
    print(f'La distancia2 o sensor de la izquierda es de {distancia2:.3f} metros')

    distancia3 = distanceSensor3.getValue()
    print(f'La distancia3 o sensor de adelante es de {distancia3:.3f} metros')


    image = color.getImage()

    r = color.imageGetRed(image, 1, 0, 0)
    g = color.imageGetGreen(image, 1, 0, 0)
    b = color.imageGetBlue(image, 1, 0, 0)

    colorsensor = colourDetector(r, g, b)
    print(f'Rojo: {r}, Verde: {g}, Azul: {b}')

    calibracionX = 0
    calibracionY = 0
    contador_de_giro = 0
    Xinicial = 0
    Yinicial = 0
    if state == "calibracion_inicial":
        print("entro al estado calibracion")
        Xinicial = round(gps.getValues()[2]/tilesize - sy, 1)
        Yinicial = round(gps.getValues()[0]/tilesize - sy, 1)
        wheel_left.setVelocity(2.0)     
        wheel_right.setVelocity(2.0)
        delay(500)
        wheel_left.setVelocity(0)     
        wheel_right.setVelocity(0)
        calibracionX = round(gps.getValues()[2]/tilesize - sy, 1)
        calibracionY = round(gps.getValues()[0]/tilesize - sy, 1)
        wheel_left.setVelocity(-2.0)     
        wheel_right.setVelocity(-2.0)
        delay(500)
        print(f"{Xinicial} != {calibracionX}")
        print(f"{Yinicial} != {calibracionY}")
        encoder_right = float(rightEncoder.getValue())
        encoder_left = float(leftEncoder.getValue())
        if Xinicial != calibracionX:
            print("paso al estado reconocimiento de Xbaldosa")
            print(f"{Xinicial} != {calibracionX}")
            calibracion_inicial = "inicio en X"
            state = "reconocimiento de Xbaldosa"
        if Yinicial != calibracionY:
            print("paso al estado reconocimiento de Ybaldosa")
            print(f"{Yinicial} != {calibracionY}")
            calibracion_inicial = "inicio en Y"
            state = "reconocimiento de Ybaldosa"
        
    if state == "calibracion_rotacion":
        print("entro al estado calibracion de rotacion")
        print(calibracion_inicial)
        if calibracion_inicial == "inicio en X":
            print(tipo_de_rotacion)
            if tipo_de_rotacion == "90_grados":
                print("paso al estado reconocimiento de Ybaldosa")
                state = "reconocimiento de Ybaldosa"
            elif tipo_de_rotacion == "180_grados":
                print("paso al estado reconocimiento de Xbaldosa")
                state = "reconocimiento de Xbaldosa"
        if calibracion_inicial == "inicio en Y":
            print(tipo_de_rotacion)
            if tipo_de_rotacion == "90_grados":
                print("paso al estado reconocimiento de Xbaldosa")
                state = "reconocimiento de Xbaldosa"
            elif tipo_de_rotacion == "180_grados":
                print("paso al estado reconocimiento de Ybaldosa")
                state = "reconocimiento de Ybaldosa"
        
    if state == "reconocimiento de Xbaldosa":
        print("estoy en el estado reconocimiento de Xbaldosa")
        calibracion_inicial = "inicio en X"
        futuro_encoder_right = encoder_right + 5.9974
        futuro_encoder_left = encoder_left + 5.9974
        state = "avanzarX"

    if state == "reconocimiento de Ybaldosa":
        print("estoy en el estado reconocimiento de Ybaldosa")
        calibracion_inicial = "inicio en Y"
        futuro_encoder_right = encoder_right + 5.9974
        futuro_encoder_left = encoder_left + 5.9974
        state = "avanzarY"

    if state == "avanzarX":
            print("estoy en el estado avanzarX")
            calibracion_inicial = "inicio en X"
            print(f"el encoder_right es {encoder_right_real} y su futuro encoder es {futuro_encoder_right}")
            print(f"el encoder_left es {encoder_left_real} y su futuro encoder es {futuro_encoder_left}")
            if encoder_right_real != futuro_encoder_right and encoder_left_real != futuro_encoder_left:
                if (encoder_right_real < futuro_encoder_right and encoder_left_real < futuro_encoder_left):
                    print("encoder_right_real < futuro_encoder_right and encoder_left_real < futuro_encoder_left")
                    wheel_left.setVelocity(3.0)     
                    wheel_right.setVelocity(3.0)
                    print(f"el encoder_right es {encoder_right_real} y su futuro encoder es {futuro_encoder_right}")
                    print(f"el encoder_left es {encoder_left_real} y su futuro encoder es {futuro_encoder_left}")
                    if distanceSensor3.getValue() <= 0.058 or colorsensor == "swamp" or colorsensor == "hole":
                        if distanceSensor1.getValue() <= 0.058:
                            if distanceSensor2.getValue() <= 0.058:
                                rotacion = "180_grados"
                                state = "deteccion de victimas"
                            elif distanceSensor2.getValue() > 0.058:
                                rotacion = "90_grados_left"
                                state = "deteccion de victimas"
                        elif distanceSensor1.getValue() > 0.058:
                            rotacion = "90_grados_right"
                            state = "deteccion de victimass"
                elif (encoder_right_real > futuro_encoder_right) and (encoder_left_real > futuro_encoder_left):
                    print("encoder_right_real > futuro_encoder_right and encoder_left_real > futuro_encoder_left")
                    wheel_left.setVelocity(0)     
                    wheel_right.setVelocity(0)
                    futuro_encoder_right = encoder_right_real
                    futuro_encoder_left = encoder_left_real
                    
            elif (encoder_right_real == futuro_encoder_right and encoder_left_real == futuro_encoder_left):
                print("encoders = futuros encoders")
                rotacion = "no hay rotacion"
                wheel_left.setVelocity(0)     
                wheel_right.setVelocity(0)
                encoder_right = encoder_right_real
                encoder_left = encoder_left_real
                state = "deteccion de victimas"


    if state == "avanzarY":
            print("estoy en el estado avanzarY")
            calibracion_inicial = "inicio en Y"
            print(f"el encoder_right es {encoder_right_real} y su futuro encoder es {futuro_encoder_right}")
            print(f"el encoder_left es {encoder_left_real} y su futuro encoder es {futuro_encoder_left}")
            if encoder_right_real != futuro_encoder_right and encoder_left_real != futuro_encoder_left:
                if (encoder_right_real < futuro_encoder_right) and (encoder_left_real < futuro_encoder_left):
                    print("encoder_right_real < futuro_encoder_right and encoder_left_real < futuro_encoder_left")
                    wheel_left.setVelocity(3.0)     
                    wheel_right.setVelocity(3.0)
                    print(f"el encoder_right es {encoder_right_real} y su futuro encoder es {futuro_encoder_right}")
                    print(f"el encoder_left es {encoder_left_real} y su futuro encoder es {futuro_encoder_left}")
                    if distanceSensor3.getValue() <= 0.058 or colorsensor == "swamp" or colorsensor == "hole":
                        if distanceSensor1.getValue() <= 0.058:
                            if distanceSensor2.getValue() <= 0.058:
                                rotacion = "180_grados"
                                state = "deteccion de victimas"
                            elif distanceSensor2.getValue() > 0.058:
                                rotacion = "90_grados_left"
                                state = "deteccion de carteles"
                        elif distanceSensor1.getValue() > 0.058:
                            rotacion = "90_grados_right"
                            state = "deteccion de victimas"
                elif encoder_right_real > futuro_encoder_right and encoder_left_real > futuro_encoder_left:
                    print("encoder_right_real > futuro_encoder_right and encoder_left_real > futuro_encoder_left")
                    wheel_left.setVelocity(0)     
                    wheel_right.setVelocity(0)
                    futuro_encoder_right = encoder_right_real
                    futuro_encoder_left = encoder_left_real
            elif (encoder_right_real == futuro_encoder_right and encoder_left_real == futuro_encoder_left):
                print("encoders = futuros encoder")
                rotacion = "no hay rotacion"
                wheel_left.setVelocity(0)     
                wheel_right.setVelocity(0)
                encoder_right = encoder_right_real
                encoder_left = encoder_left_real
                state = "deteccion de victimas"

                

    if state == "rotar_180_grados":
            print("Girando 180 grados")
            turn_gyro(180, 0.5) 
            w_velocity(0.0)
            tipo_de_rotacion = "180_grados"
            encoder_right = encoder_right_real
            encoder_left = encoder_left_real
            encoder_right -= 4.35204
            encoder_left += 4.5216
            state = "calibracion_rotacion"

    if state == "rotar_a_la_izquierda":
            print("Girando a la izquierda")
            turn_gyro(90, -0.5) 
            w_velocity(0.0)
            tipo_de_rotacion = "90_grados"
            encoder_right = encoder_right_real
            encoder_left = encoder_left_real
            encoder_right += 2.28592
            encoder_left -= 2.12264
            state = "calibracion_rotacion"
            

    if state == "rotar_a_la_derecha":
            print("Girando a la derecha")
            turn_gyro(90, 0.5) 
            w_velocity(0.0)
            tipo_de_rotacion = "90_grados"
            encoder_right = encoder_right_real
            encoder_left = encoder_left_real
            encoder_right -= 2.12264
            encoder_left += 2.28592
            state = "calibracion_rotacion"

    if state == "deteccion de victimas":
        print("deteccion de victimas")
        C1 = Camera1.getImage()
        C2 = Camera2.getImage()
        if rotacion == "180_grados":
            if checkVic1(C1):
                print("¡Detectada!")
                classifyVictim1(C1)
                print("paso a rotar_180_grados")
                state = "rotar_180_grados"
            elif checkVic2(C2):
                print("¡Detectada!")
                classifyVictim1(C2)
                print("paso a rotar_180_grados")
                state = "rotar_180_grados"
            else:
                print("paso a rotar_180_grados")
                state = "rotar_180_grados"

        if rotacion == "90_grados_right":
            if checkVic1(C1):
                print("¡Detectada!")
                classifyVictim1(C1)
                print("paso a rotar_a_la_derecha")
                state = "rotar_a_la_derecha"
            else:
                print("paso a rotar_a_la_derecha")
                state = "rotar_a_la_derecha"

        if rotacion == "90_grados_left":
            if checkVic1(C2):
                print("¡Detectada!")
                classifyVictim1(C2)
                print("paso a rotar_a_la_izquierda")
                state = "rotar_a_la_izquierda"
            else:
                print("paso a rotar_a_la_izquierda")
                state = "rotar_a_la_izquierda"

        else:
            if calibracion_inicial == "inicio en X":
                if checkVic1(C1):
                    print("¡Detectada!")
                    classifyVictim1(C1)
                    print("paso a reconocimiento de Xbladosa")
                    state = "reconocimiento de Xbaldosa"
                elif checkVic2(C2):
                    print("¡Detectada!")
                    classifyVictim1(C2)
                    print("paso a reconocimiento de Xbladosa")
                    state = "reconocimiento de Xbaldosa"
                else:
                    print("paso a reconocimiento de Xbladosa")
                    state = "reconocimiento de Xbaldosa"

            if calibracion_inicial == "inicio en Y":
                if checkVic1(C1):
                    print("¡Detectada!")
                    classifyVictim1(C1)
                    print("paso a reconocimiento de Ybladosa")
                    state = "reconocimiento de Ybaldosa"
                elif checkVic2(C2):
                    print("¡Detectada!")
                    classifyVictim1(C2)
                    print("paso a reconocimiento de Ybladosa")
                    state = "reconocimiento de Ybaldosa"
                else:
                    print("paso a reconocimiento de Ybladosa")
                    state = "reconocimiento de Ybaldosa"


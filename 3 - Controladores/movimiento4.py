#Cargo controladores
from controller import Robot, Motor, GPS, DistanceSensor, Camera, Gyro
import math

tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep())
angulo_actual = 0 

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

#Funciones:
def delay(ms):
    initTime = robot.getTime()
    while robot.step(timeStep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

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
        calibracion_inicial = "inicio en X"
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
                                state = "rotar_180_grados"
                            elif distanceSensor2.getValue() > 0.058:
                                state = "rotar_a_la_izquierda"
                        elif distanceSensor1.getValue() > 0.058:
                            state = "rotar_a_la_derecha"
                elif (encoder_right_real > futuro_encoder_right) and (encoder_left_real > futuro_encoder_left):
                    print("encoder_right_real > futuro_encoder_right and encoder_left_real > futuro_encoder_left")
                    wheel_left.setVelocity(0)     
                    wheel_right.setVelocity(0)
                    futuro_encoder_right = encoder_right_real
                    futuro_encoder_left = encoder_left_real
                    
            elif (encoder_right_real == futuro_encoder_right and encoder_left_real == futuro_encoder_left):
                print("encoders = futuros encoders")
                wheel_left.setVelocity(0)     
                wheel_right.setVelocity(0)
                encoder_right = encoder_right_real
                encoder_left = encoder_left_real
                delay(1000)
                state = "reconocimiento de Xbaldosa"


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
                                state = "rotar_180_grados"
                            elif distanceSensor2.getValue() > 0.058:
                                state = "rotar_a_la_izquierda"
                        elif distanceSensor1.getValue() > 0.058:
                            state = "rotar_a_la_derecha"
                elif encoder_right_real > futuro_encoder_right and encoder_left_real > futuro_encoder_left:
                    print("encoder_right_real > futuro_encoder_right and encoder_left_real > futuro_encoder_left")
                    wheel_left.setVelocity(0)     
                    wheel_right.setVelocity(0)
                    futuro_encoder_right = encoder_right_real
                    futuro_encoder_left = encoder_left_real
            elif (encoder_right_real == futuro_encoder_right and encoder_left_real == futuro_encoder_left):
                print("encoders = futuros encoder")
                wheel_left.setVelocity(0)     
                wheel_right.setVelocity(0)
                encoder_right = encoder_right_real
                encoder_left = encoder_left_real
                delay(1000)
                state = "reconocimiento de Ybaldosa"

                

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


#Cargo controladores
from controller import Robot, Motor, GPS, DistanceSensor, Camera
import math

tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep())
angulo_actual = 0 

#Motores:
wheel_left = robot.getDevice("wheel1 motor")    
wheel_right = robot.getDevice("wheel2 motor")

wheel_left.setPosition(float('inf')) 
wheel_right.setPosition(float('inf'))

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
start = robot.getTime() #Preguntar al profe que es
robot.step(timeStep) 

sy = gps.getValues()[0]/tilesize 
sx = gps.getValues()[0]/tilesize 

state = "avanzar"
while robot.step(timeStep) != -1: 
    
    y = round(gps.getValues()[0]/tilesize - sy, 1) 
    x = round(gps.getValues()[2]/tilesize - sx, 1) 

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

    if state == "avanzar":
        if distanceSensor3.getValue() <= 0.058 or colorsensor == "swamp" or colorsensor == "hole":
            if distanceSensor1.getValue() <= 0.058:
                if distanceSensor2.getValue() <= 0.058:
                    state = "rotar_180_grados"
                elif distanceSensor2.getValue() > 0.058:
                    state = "rotar_a_la_izquierda"
            elif distanceSensor1.getValue() > 0.058:
                state = "rotar_a_la_derecha"
        else:
            wheel_left.setVelocity(1.0)     
            wheel_right.setVelocity(1.0)

    if state == "rotar_180_grados":
        turn_gyro(180, 0.5) 
        w_velocity(0.0)
        print("Girando 180 grados")
        state = "avanzar"

    if state == "rotar_a_la_izquierda":
        turn_gyro(90, 0.5) 
        w_velocity(0.0)
        print("Girando a la izquierda")
        state = "avanzar"

    if state == "rotar_a_la_derecha":
        turn_gyro(90, -0.5) 
        w_velocity(0.0)
        print("Girando a la derecha")
        state = "avanzar"
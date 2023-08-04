''' Controlador para detectar colores '''

from controller import Robot, Camera, Motor, DistanceSensor
import math

robot = Robot()
state = 'avanzar'
angulo_actual = 0

timeStep = int(robot.getBasicTimeStep())

wheel_left = robot.getDevice('wheel2 motor')
wheel_right = robot.getDevice('wheel1 motor')

wheel_left.setPosition(float('inf'))
wheel_right.setPosition(float('inf'))

d_sensor = robot.getDevice('distance sensor1')
d_sensor.enable(timeStep)

gyro = robot.getDevice('gyro')
gyro.enable(timeStep)

color = robot.getDevice("colour_sensor")
color.enable(timeStep)

def w_velocity(vel):
    wheel_left.setVelocity(vel)
    wheel_right.setVelocity(vel)

def turn(vel):
    wheel_left.setVelocity(vel)
    wheel_right.setVelocity(-vel)

def turn_gyro(angle, velTurn):
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
    if (180 <= r <= 190) and (145 <= g <= 155) and (80 <= b <= 90):
        color = "Swamp"
    elif (65 <= r <= 70) and (70 <= g <= 80) and (89 <= b <=93):
        color = "Checkpoint"
    elif (r and g and b) <= 35:
        color = "Hole"
    return color        

while robot.step(timeStep) != -1:
    
    image = color.getImage()

    r = color.imageGetRed(image, 1, 0, 0)
    g = color.imageGetGreen(image, 1, 0, 0)
    b = color.imageGetBlue(image, 1, 0, 0)

    detectColor = colourDetector(r, g, b)

    if state == 'avanzar':
        if d_sensor.getValue() <= 0.045 or detectColor == 'Swamp':
            state = 'rotar'
        else:
            w_velocity(1.0)
            print(detectColor)

    if state == 'rotar':
        turn_gyro(90, 0.5)
        print("Girando...")
        state = 'avanzar'
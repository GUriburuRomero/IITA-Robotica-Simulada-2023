
from controller import Robot, Motor
import math

tilesize = 0.06
state = 'rotar'

robot = Robot()
timeStep = int(robot.getBasicTimeStep())
angulo_actual = 0

wheel_left = robot.getDevice('wheel2 motor')
wheel_right = robot.getDevice('wheel1 motor')

wheel_left.setPosition(float('inf'))
wheel_right.setPosition(float('inf'))

gyro = robot.getDevice('gyro')
gyro.enable(timeStep)

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

while robot.step(timeStep) != -1:
    
    if state == 'rotar':
        turn_gyro(90, 0.5) # Cambiar el signo del segundo parámetro para cambiar de dirección
        w_velocity(0.0)
        break
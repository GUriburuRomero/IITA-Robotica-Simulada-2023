from controller import Robot, Motor, PositionSensor
import math

tilesize = 0.06
state = 'rotar'
noventaGrados = 2.25 # 2.31 con timeStep = 32

robot = Robot()
timeStep = int(robot.getBasicTimeStep())
angulo_actual = 0

wheel_left = robot.getDevice('wheel2 motor')
wheel_right = robot.getDevice('wheel1 motor')

wheel_left.setPosition(float(noventaGrados))
wheel_right.setPosition(float('inf'))

l_enc = wheel_left.getPositionSensor()
r_enc = wheel_right.getPositionSensor()

l_enc.enable(timeStep)
r_enc.enable(timeStep)

def w_velocity(vel):
    ''' Permite avanzar hacia adelante al robot '''
    wheel_left.setVelocity(vel)
    wheel_right.setVelocity(vel)

def turn(vel):
    ''' Permite rotar sobre su eje al robot'''
    wheel_left.setVelocity(-vel)
    wheel_right.setVelocity(vel)

while robot.step(timeStep) != -1:
    
    if state == 'rotar':
        wheel_left.setPosition(float(noventaGrados)) # Para girar al otro lado: 1. posicionar la otra rueda en noventaGrados
        turn(-0.2) # 2. cambiar el signo de la constante -0.2 (la velocidad)

        print(f'Diferencia del encoder: {abs(l_enc.getValue()-noventaGrados)}')

        if (abs(l_enc.getValue() - noventaGrados)) <= 0.01: # 3. Realizar la operación con el otro encoder
            wheel_left.setPosition(float('inf'))
            turn(0.0)
            print("¡He terminado!")
            break


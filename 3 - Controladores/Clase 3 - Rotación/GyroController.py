from controller import Robot
import math

tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep()) 

angulo_actual = 0

estado = "rotar"

wheel1 = robot.getDevice("wheel1 motor") 
wheel2 = robot.getDevice("wheel2 motor") 

wheel1.setPosition(float('inf'))
wheel2.setPosition(float('inf'))

gyro = robot.getDevice('gyro')
gyro.enable(timeStep)

def avanzar(vel):
    wheel1.setVelocity(vel)
    wheel2.setVelocity(vel)

def girar(vel):
    wheel1.setVelocity(-vel)
    wheel2.setVelocity(vel)

def rotar(angulo):
    global angulo_actual
    tiempo_anterior = 0

    girar(0.5)
    # Mientras no llego al angulo solicitado sigo girando con una precision de 1 grado
    while ( abs(angulo - angulo_actual) > 1):

        tiempo_actual = robot.getTime()
        tiempo_transcurrido = tiempo_actual - tiempo_anterior 

        radsIntimestep = abs(gyro.getValues()[1]) * tiempo_transcurrido
        degsIntimestep = radsIntimestep * 180 / math.pi 

        print(f"rads: {radsIntimestep:.3f} | degs: {degsIntimestep:.3f}")

        angulo_actual += degsIntimestep

        # Si se pasa de 360 grados se ajusta la rotacion empezando desde 0 grados
        angulo_actual = angulo_actual % 360
        # Si es mas bajo que 0 grados, le resta ese valor a 360
        if angulo_actual < 0:
            angulo_actual += 360

        tiempo_anterior = tiempo_actual
        robot.step(timeStep)

    print("Rotacion finalizada.")
    avanzar(0)
    return True

while robot.step(timeStep) != -1: 
    if estado == 'rotar':
        rotar(180)
        estado = 'avanzar'

    elif estado == 'avanzar':
        avanzar(0.4)
from controller import Robot, Motor, PositionSensor

robot = Robot()

timeStep = 32

noventaGrados = 2.5

coGrados = 4.75

tilesize = 0.06
estado = "Girar"

ruedaIzquierda = robot.getDevice("wheel1 motor")
ruedaDerecha = robot.getDevice("wheel2 motor")

ruedaIzquierda.setPosition(float('inf'))
ruedaDerecha.setPosition(float('inf'))

leftEnc = ruedaIzquierda.getPositionSensor()    
rightEnc = ruedaDerecha.getPositionSensor()

leftEnc.enable(timeStep)
rightEnc.enable(timeStep)

robot.step(timeStep)

def turn(vel):
    'Gira el robot sobre su propio eje'
    ruedaIzquierda.setVelocity(vel)
    ruedaDerecha.setVelocity(-vel)

while robot.step(timeStep) != -1: 
    if estado == 'Girar':
        turn(0.2)
        print("Diferencia del encoder:", leftEnc.getValue() - noventaGrados)

        if(abs(leftEnc.getValue() - noventaGrados > 0.01) and estado == "Girar"):
            turn(0)

from controller import Robot
from controller import DistanceSensor

tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep()) 

distanceSensor = robot.getDevice("Sd")
distanceSensor.enable(timeStep)

while robot.step(timeStep) != -1:
    
    distancia = distanceSensor.getValue()
    print(f'La distancia es de {distancia:.3f} metros')
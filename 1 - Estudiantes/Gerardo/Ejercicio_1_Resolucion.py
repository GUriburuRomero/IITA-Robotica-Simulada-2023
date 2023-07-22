from controller import Robot, GPS, Motor 

tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep()) 

gps = robot.getDevice("gps") 
gps.enable(timeStep) 

wheel1 = robot.getDevice("wheel1 motor") 
wheel2 = robot.getDevice("wheel2 motor") 

wheel1.setPosition(float('inf'))
wheel2.setPosition(float('inf'))

start = robot.getTime() 
robot.step(timeStep) 

sx = gps.getValues()[0]/tilesize 

def wheelsVelocity(vel):
    '''Creo una función para evitar ser recursivo'''
    wheel1.setVelocity(vel)
    wheel2.setVelocity(vel)
                       
while robot.step(timeStep) != -1: 
    
    x = round(gps.getValues()[2]/tilesize - sx, 1) 

    if x != 1.2:
        wheelsVelocity(0.7)
    else:
        print(f"¡He llegado! Punto: {x}")
        wheelsVelocity(0.0)
        break
from controller import Robot, GPS 

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

sy = gps.getValues()[0]/tilesize 
sx = gps.getValues()[0]/tilesize 

while robot.step(timeStep) != -1: 
    
    y = round(gps.getValues()[0]/tilesize - sy, 1) 
    x = round(gps.getValues()[2]/tilesize - sx, 1) 

    print(f'x: {x}, y: {y}')

from controller import Robot
from controller import Motor
from controller import GPS

tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep()) 

wheel_left = robot.getDevice("wheel1 motor")     #Step 1
wheel_right = robot.getDevice("wheel2 motor")

wheel_left.setPosition(float('inf'))    #Step 2
wheel_right.setPosition(float('inf'))

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

    wheel_left.setVelocity(1)     #Step 3
    wheel_right.setVelocity(1)
    if x == 1.4 and y == 0:
        wheel_left.setVelocity(0)     
        wheel_right.setVelocity(0)
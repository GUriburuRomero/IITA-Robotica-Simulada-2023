from controller import Robot
from controller import Motor

tilesize = 0.05 
robot = Robot() 
timeStep = int(robot.getBasicTimeStep()) 

wheel_left = robot.getDevice("wheel1 motor")     #Step 1
wheel_right = robot.getDevice("wheel2 motor")

wheel_left.setPosition(float('inf'))    #Step 2
wheel_right.setPosition(float('inf'))

while robot.step(timeStep) != -1:
    wheel_left.setVelocity(1.0)     #Step 3
    wheel_right.setVelocity(1.0)
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

sy = gps.getValues()[1]/tilesize 
sx = gps.getValues()[0]/tilesize 

wheel1.setPosition(float('inf'))    #Step 2
wheel2.setPosition(float('inf'))


while robot.step(timeStep) != -1: 
    
    y = round(gps.getValues()[0]/tilesize - sy, 1) 
    x = round(gps.getValues()[2]/tilesize - sx, 1) 
    wheel1.setVelocity(1.0)     #Step 3
    wheel2.setVelocity(1.0)
    if y== -7.0 and x== 1.4: 
        wheel1.setVelocity(0.0)
        wheel2.setVelocity(0.0)
    print(f'x: {x}, y: {y}')

from controller import Robot, GPS

timeStep = 32 
tilesize = 0.065

robot = Robot()

gps = robot.getDevice("gps")
gps.enable(timeStep)

wheel1 = robot.getDevice("wheel1 motor")
wheel2 = robot.getDevice("wheel2 motor")

start = robot.getTime()

while robot.step(timeStep) != -1:

    x = round(gps.getValues()[0]/tilesize)
    y = round(gps.getValues()[1]/tilesize)
    z = round(gps.getValues()[2]/tilesize)

    print(f'x: {x}, y: {y}, z: {z}')
''' Controlador para el sensor de color '''

from controller import Robot, Camera

robot = Robot()

timeStep = int(robot.getBasicTimeStep())

color = robot.getDevice("colour_sensor")
color.enable(timeStep)

while robot.step(timeStep) != -1:
    
    image = color.getImage()

    r = color.imageGetRed(image, 1, 0, 0)
    g = color.imageGetGreen(image, 1, 0, 0)
    b = color.imageGetBlue(image, 1, 0, 0)

    print(f'Rojo: {r}, Verde: {g}, Azul: {b}')
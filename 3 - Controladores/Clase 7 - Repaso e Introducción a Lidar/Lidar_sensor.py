from controller import Robot, Lidar

robot = Robot()
 
timeStep = int(robot.getBasicTimeStep())

lidar = robot.getDevice("lidar")
lidar.enable(timeStep)

lidar.enablePointCloud()

while robot.step(timeStep) != -1:
    lidarPoints = lidar.getPointCloud(); # Get the point cloud

    # Print out the x, y, z, and layer information for the first point in the point cloud    
    print(f"x: + {(lidarPoints[0].x):.3}  y: {(lidarPoints[1].y):.3} z: {(lidarPoints[2].z):.3}")
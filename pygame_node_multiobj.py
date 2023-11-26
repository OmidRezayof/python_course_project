import rospy
from geometry_msgs.msg import Point
import math
import numpy as np
import random
import pygame
import sys

# Initialize Pygame
pygame.init()


num_of_sheeps=0
goal_vel=1
obj_vel=1


# Pygame window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


spot_loc=[0,0]
goal_loc=[0,200]
obj_loc=[0,10]


# Initialize Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('ROS Node Data')

def polar2cart(r,theta,xc,yc):
    x=0
    y=0
    x=r*math.cos(theta)+xc
    y=r*math.sin(theta)+yc
    return x,y,

num_of_sheeps=4
sheeps_loc=np.zeros([num_of_sheeps,2])
herd_radius=10

for i in range(0,num_of_sheeps):
    sheeps_loc[i][0]=random.uniform(-3.14, 3.14)
    sheeps_loc[i][1]=random.uniform(0.2, herd_radius)

for i in range(0,num_of_sheeps):
    sign[i]=random.choice([-1,1])
def herd(xc,yc):
    global num_of_sheeps,screen,BLUE,WINDOW_HEIGHT,WINDOW_WIDTH,herd_radius,counter,sign
    counter=counter+1
    if(counter==100):
        counter=0
        for i in range(0,num_of_sheeps):
            sign[i]=random.choice([-1,1])    
    for i in range(0,num_of_sheeps):
        sheeps_loc[i][0]=sheeps_loc[i][0]+sign[i]*(random.uniform(0, 1.0))/60
        sheeps_loc[i][1]=abs(sheeps_loc[i][1]+random.uniform(-0.15,0.2))
        if sheeps_loc[i][1]>herd_radius:
            sheeps_loc[i][1]=herd_radius
        a,b,=polar2cart(sheeps_loc[i][1], sheeps_loc[i][0], xc, yc)
        pygame.draw.circle(screen, BLUE, (WINDOW_WIDTH/2+(a), WINDOW_HEIGHT/2-b),2)
    return



# ROS callback functions for each topic
def spot_loc_callback(data):
    global spot_loc,old_sloc
    spot_loc[0] = data.x
    spot_loc[1] = data.y
    

def goal_loc_callback(data):
    global goal_loc,old_gloc
    goal_loc[0] = data.x
    goal_loc[1] = data.y

def obj_loc_callback(data):
    global obj_loc,old_oloc
    obj_loc[0] = data.x
    obj_loc[1] = data.y

# Initialize ROS node
rospy.init_node('pygame_ros_node')

# Subscribe to ROS topics
rospy.Subscriber('spot_loc_topic', Point, spot_loc_callback)
rospy.Subscriber('goal_loc_topic', Point, goal_loc_callback)
rospy.Subscriber('obj_loc_topic', Point, obj_loc_callback)

# Pygame clock
clock = pygame.time.Clock()

# Main loop
while not rospy.is_shutdown():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rospy.signal_shutdown('Quit requested by user')
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Draw points if they are received from ROS topics
    pygame.draw.circle(screen, RED, (WINDOW_WIDTH/2+int(spot_loc[0]), WINDOW_HEIGHT/2-int(spot_loc[1])), 2)
    pygame.draw.circle(screen, GREEN, (WINDOW_WIDTH/2+int(goal_loc[0]), WINDOW_HEIGHT/2-int(goal_loc[1])), 2)
    herd(obj_loc[0],obj_loc[1])
    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Exit Pygame
pygame.quit()

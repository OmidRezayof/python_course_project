#!/usr/bin/env python

import rospy
import copy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Point


goal_loc = [0, 200]

RTS_pointing = [0, 0]



def position(data):
    global RTS_pointing,goal_loc
    
    RTS_pointing[0] = -data.axes[3]
    RTS_pointing[1] = data.axes[4]
    
    temp = (RTS_pointing[0]**2 + RTS_pointing[1]**2)**0.5
    if temp != 0:
        RTS_pointing[0] /= temp
        RTS_pointing[1] /= temp

    publishing_msg = Point()
    goal_vel = 0.5

    goal_loc[0] += RTS_pointing[0] * goal_vel
    goal_loc[1] += RTS_pointing[1] * goal_vel

    publishing_msg.x = goal_loc[0]
    publishing_msg.y = goal_loc[1]
    publishing_msg.z = 0 
    
    if not rospy.is_shutdown():
        pub.publish(publishing_msg)    



if __name__ == '__main__':
    rospy.init_node('goal_loc_node')

    rate = rospy.Rate(5)  # ROS Rate at 5Hz
    pub = rospy.Publisher('goal_loc_topic', Point, queue_size=10)
    rospy.Subscriber("joy", Joy, position)
    
    while not rospy.is_shutdown():
        rate.sleep()


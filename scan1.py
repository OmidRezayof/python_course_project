# -*- coding: utf-8 -*-
import math
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point
from numpy import array,inf
import numpy as np

def locations(msg):
    #whatever
    #msg.ranges is the ranges array
    dists = list(msg.ranges)
    # depth = 5 #arbitrary value, may need to find the depth of the husky based on range readings
    min_ang = msg.angle_min
    #print(min_ang)
    ang_inc = msg.angle_increment
    #print(ang_inc)
    publishing_msg = Point()
    sensor_pubmsg=Point()

    for i in range(len(dists)):
    
        if dists[i] == inf or dists[i] == -inf:
            dists[i] = 0 
            
    #need to get rid of the inf values to be able to process data
    if(dists==list(np.zeros(len(dists)))):
        obj_dist = 0
    else:
        obj_dist = min(value for value in dists if value != 0)
    #print(dists)
    #print('obj_dist',obj_dist)
    obj_ind = dists.index(obj_dist)
    #print('obj_ind',obj_ind)
    #print(len(dists))
    obj_ang = ang_inc*obj_ind  #should be object angle in radians
    #print("obj_ang", obj_ang)
    obj_x = obj_dist*math.cos(obj_ang+min_ang)
    #print("obj_x", obj_x)
    obj_y = obj_dist*math.sin(-min_ang+obj_ang)
    #print("obj_y",obj_y)
    obj_loc = [obj_x, obj_y] 
    #obj_loc should have the x, y coordinates of the object with respect to the lidar
    #may not need goal_loc if we use the joystick to control the goal
    
    goal_dist = max(dists)
    goal_ind = dists.index(goal_dist)
    goal_angle = ang_inc*goal_ind
    x_s = goal_dist*math.cos(goal_angle+min_ang)
    y_s = goal_dist*math.sin(-min_ang-goal_angle)

    goal_loc = [x_s,y_s]
    publishing_msg.x=obj_x
    publishing_msg.y=obj_y
    publishing_msg.z = obj_dist
    sensor_pubmsg.x=x_s
    sensor_pubmsg.y=y_s
    sensor_pubmsg.z=((x_s-obj_x)**2+(y_s-obj_y)**2)**0.5
    if not rospy.is_shutdown():
        pub.publish(publishing_msg)
        pub2.publish(sensor_pubmsg)

    #goal_loc should have the average of the 2 furthest distance readings

if __name__ == '__main__':
    rospy.init_node('scan_values')

    rate = rospy.Rate(5)  # ROS Rate at 5Hz
    sub = rospy.Subscriber('/front/scan',LaserScan, locations)
    pub = rospy.Publisher('lidar_topic_obj', Point, queue_size=10)
    pub2 = rospy.Publisher('lidar_topic_goal', Point, queue_size=10)
    #don't want to mess up his algorithm and don't know how to use the global variables to do this publishing
    
    while not rospy.is_shutdown():
        rate.sleep()

#find the ros node and package with:
#rostopic list
#find the laser/scan topic
#rostopic echo </whatever the topic you found before was> -nl
#rostopic info </whatever the laser scan topic is>
#find what msg it is with the Type: <sensor_msgs/LaserScan>
#rosmsg show <sensor_msgs/LaserScan>
#we want to use the ranges array and the min and max angle and angle increment
#ranges contains the values for the different beams in the laser

#launch file
# <launch>
#     <node pkg = 'laser_values' type = 'scan.py' name = 'scan_values' output = 'screen'>

#     <node>
# <launch>

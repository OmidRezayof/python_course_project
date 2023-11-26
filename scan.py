# -*- coding: utf-8 -*-
import math
import rospy
from sensor_msgs.msg import LaserScan
#from geometry_msg.msg import Point

def locations(msg):
    #whatever
    #msg.ranges is the ranges array
    dists = msg.ranges
    depth = 5 #arbitrary value, may need to find the depth of the husky based on range readings
    min_ang = msg.angle_min
    ang_inc = msg.angle_inc
    
    for i in range(len(dists)):
        if dists[i] == 'inf':
            dists[i] = 0 
    #need to get rid of the inf values to be able to process data
    
    obj_dist = min(value for value in dists if value != 0)
    obj_ind = dists.index(obj_dist)
    obj_ang = min_ang + ang_inc*obj_ind  #should be object angle in radians
    obj_x = obj_dist*math.cos(obj_ang)
    obj_y = obj_dist*math.sin(obj_ang)
    obj_loc = [obj_x, obj_y] 
    #obj_loc should have the x, y coordinates of the object with respect to the lidar
    n = 0 
    goal = [[0,0,[0,0]]]
    while n < 2: #going to find 2 max distances to use as goal posts
        dist = max(dists)
        ind = dists.index(dist)
        angle = min_ang + ang_inc*ind
        x = dist*math.cos(angle)
        y = dist*math.sin(angle)
        dists[ind] = 0
        goal[n] = [x,y]
        n = n+1
    x_s = (goal[0][0]+goal[1][0])/2
    y_s = (goal[0][1]+goal[1][1])/2
    goal_loc = [x_s,y_s]
    #goal_loc should have the average of the 2 furthest distance readings

if __name__ == '__main__':
    rospy.init_node('scan_values')

    rate = rospy.Rate(5)  # ROS Rate at 5Hz
    sub = rospy.Subscriber('/kobuki/laser/scan',LaserScan, locations)
    #pub = rospy.Publisher('goal_loc_topic', Point, queue_size=10)
    #pub = rospy.Publisher('obj_loc_topic', Point, queue_size=10)
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

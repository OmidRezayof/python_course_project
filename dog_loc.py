#!/usr/bin/env python

import rospy
import copy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Point

spot_loc = [0, 0]
obj_loc = [0,35] # should be fed with the sensor. for now, I'm reading it with subscription
goal_loc = [0, 200]
visibility_threshold=50


def goal_update(data):

    global goal_loc
    goal_loc[0]=data.x
    goal_loc[1]=data.y

    return

def obj_update(data):

    global obj_loc
    obj_loc[0]=data.x
    obj_loc[1]=data.y

    return


def pos_process():
    publishing_msg = Point()
    global spot_loc, obj_loc, goal_loc
    
    robot_object_distance = 35
    
    goal_obj_dist=((obj_loc[0] - goal_loc[0])**2+(obj_loc[1] - goal_loc[1])**2)**0.5
    spot_obj_dist=((obj_loc[0] - spot_loc[0])**2+(spot_loc[1] - obj_loc[1])**2)**0.5
   

    
    if spot_obj_dist<visibility_threshold and goal_obj_dist>4:
        spot_loc[0] = obj_loc[0] - goal_loc[0]
        spot_loc[1] = obj_loc[1] - goal_loc[1]
        temp = (spot_loc[0]**2 + spot_loc[1]**2)**0.5
        spot_loc[0] = obj_loc[0] + robot_object_distance * spot_loc[0] / temp
        spot_loc[1] = obj_loc[1] + robot_object_distance * spot_loc[1] / temp

    publishing_msg.x = spot_loc[0]
    publishing_msg.y = spot_loc[1]
    publishing_msg.z = 0


    if not rospy.is_shutdown():
        pub.publish(publishing_msg)
    



    
    
if __name__ == '__main__':
    rospy.init_node('position_node')

    rate = rospy.Rate(5)  # ROS Rate at 5Hz
    pub = rospy.Publisher('spot_loc_topic', Point, queue_size=10)
    rospy.Subscriber("obj_loc_topic", Point, obj_update)
    rospy.Subscriber("goal_loc_topic", Point, goal_update)

    while not rospy.is_shutdown():
        pos_process()
        rate.sleep()


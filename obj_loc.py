#!/usr/bin/env python

import rospy
import copy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Point

obj_loc = [0, 20]
goal_loc = [0, 200]
LTS_pointing = [0, 0]
obj_pointing=[0,0]
spot_loc=[0,0]



def goal_update(data):

    goal_loc[0]=data.x
    goal_loc[1]=data.y

    return

def spot_loc_update(data):

    spot_loc[0]=data.x
    spot_loc[1]=data.y

    return




def pos_process():
    publishing_msg = Point()
    global obj_loc, goal_loc, LTS_pointing,obj_pointing
    object_vel = 0.5  # a number between 0-1

    if(LTS_pointing==[0,0]):
        if(((obj_loc[0] - goal_loc[0])**2+(obj_loc[1] - goal_loc[1])**2)**0.5<5):
            print ("sufficiently close")
            return
        obj_pointing[0]=(obj_loc[0]-spot_loc[0])
        obj_pointing[1]=(obj_loc[1]-spot_loc[1])
        temp = (obj_pointing[0]**2+obj_pointing[1]**2)**0.5
        obj_pointing[0]=obj_pointing[0]/temp
        obj_pointing[1]=obj_pointing[1]/temp
    else:
        obj_pointing=copy.copy(LTS_pointing)

    obj_loc[0] += obj_pointing[0] * object_vel
    obj_loc[1] += obj_pointing[1] * object_vel

    publishing_msg.x=obj_loc[0]
    publishing_msg.y=obj_loc[1]
    publishing_msg.z=0

    if not rospy.is_shutdown():
        pub.publish(publishing_msg)
    




def position(data):
    global LTS_pointing
    LTS_pointing[0] = -data.axes[0]
    LTS_pointing[1] = data.axes[1]
    
    temp = (LTS_pointing[0]**2 + LTS_pointing[1]**2)**0.5
    if temp != 0:
        LTS_pointing[0] /= temp
        LTS_pointing[1] /= temp

    return

    

    
if __name__ == '__main__':
    rospy.init_node('obj_loc_node')

    rate = rospy.Rate(5)  # ROS Rate at 5Hz
    pub = rospy.Publisher('obj_loc_topic', Point, queue_size=10)
    rospy.Subscriber("joy", Joy, position)
    rospy.Subscriber("goal_loc_topic",Point, goal_update)
    rospy.Subscriber("spot_loc_topic",Point, spot_loc_update)
    
    while not rospy.is_shutdown():
        pos_process()
        rate.sleep()


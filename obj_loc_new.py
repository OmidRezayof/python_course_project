#!/usr/bin/env python

import rospy
import copy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Point, Twist
from gazebo_msgs.msg import ModelState, ModelStates


goaldist = 100
LTS_pointing = [0, 0]
obj_pointing=[0,0]
husky_loc=[0,-20]
object_vel = 1  # a number between 0-1



def goal_update(data):
    global goaldist
    goaldist=data.z

    return

def husky_loc_update(data):

    global husky_loc
    husky_loc[0]=-data.x
    husky_loc[1]=-data.y
    return




def pos_process():
    global goaldist, LTS_pointing,obj_pointing, object_vel,husky_loc
    huskydist=((husky_loc[0])**2+(husky_loc[1])**2)**0.5
    publishing_msg = Point()
    if(LTS_pointing==[0,0]):
        if(goaldist<0.5):
            print ("sufficiently close")
            return
        if(huskydist>5):
            print("too far")
            return
        obj_pointing[0]=(-husky_loc[0])
        obj_pointing[1]=(-husky_loc[1])
        temp = (obj_pointing[0]**2+obj_pointing[1]**2)**0.5
        obj_pointing[0]=obj_pointing[0]/temp
        obj_pointing[1]=obj_pointing[1]/temp
    else:
        obj_pointing=copy.copy(LTS_pointing)


    

    model_state = ModelState()
    model = rospy.wait_for_message('gazebo/model_states',ModelStates)
    for i in range(len(model.name)):
        if(model.name[i]=='our_unit_cylinder'):
            
            model_state.pose=model.pose[i]
            model_state.model_name = "our_unit_cylinder"  # Name of the model in Gazebo
            model_state.twist.linear.x = obj_pointing[0]*object_vel
            model_state.twist.linear.y = obj_pointing[1]*object_vel
            model_state.twist.linear.z = 0
            model_state.twist.angular.x = 0
            model_state.twist.angular.y = 0
            model_state.twist.angular.z = 0
            if not rospy.is_shutdown():
                model_publisher.publish(model_state)

    
    




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
    model_publisher = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    rate = rospy.Rate(5)  # ROS Rate at 5Hz
    pub = rospy.Publisher('obj_loc_topic', Point, queue_size=10)
    rospy.Subscriber("joy", Joy, position)
    rospy.Subscriber("/lidar_topic_goal",Point, goal_update)
    rospy.Subscriber("/lidar_topic_obj",Point, husky_loc_update)
    
    while not rospy.is_shutdown():
        pos_process()
        rate.sleep()


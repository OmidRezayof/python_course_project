# -*- coding: utf-8 -*-
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
from math import tan
from math import sin
from math import cos
from math import sqrt
import time

flag = 0
flag2=0
flag3=0
flag4 = 0
flag5 = 0
init_x = 0.0
init_y = 0.0 
init_theta = 0.0
x = 0
y = 0
theta = 0
goal_loc=[0,0]
obj_loc = [0,0]
called=2
update = 0
#need to write another script to get the initial odometry and theta only once then
#subtract those values from the newOdom updating x and y 
#x and y need to be the odometry reading - the initial odometry reading when husky is asked to move to x
def goal_update(msg):
    global goal_loc,called, update
    global flag2
    if flag2 == 0:
        goal_loc[0] = msg.x
        #print("test")
        goal_loc[1] = msg.y
        flag2 = 1
        update = update + 1
def obj_update(msg):
    global obj_loc ,called, update
    global flag3
    if flag3 == 0:
            
        #print("test2")
        obj_loc[0] = msg.x
        print(msg.x)
        obj_loc[1] = msg.y
        print(msg.y)
        flag3 = 1
        update = update + 1
        #print(called)
def newOdom(msg):
    global flag, init_x, init_y, init_theta, x, y, theta
    if flag==0:
        init_x = msg.pose.pose.position.x
        init_y = msg.pose.pose.position.y
        rot_q = msg.pose.pose.orientation
        (roll, pitch, init_theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
        flag = 1
        
    if flag ==1:
        x = msg.pose.pose.position.x - init_x 
        y = msg.pose.pose.position.y - init_y
        rot_q = msg.pose.pose.orientation
        (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
        
        theta = theta - init_theta
         
    
if __name__ == '__main__':
    rospy.init_node("speed_controller")

    sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
    sub2 = rospy.Subscriber('/lidar_topic_goal',Point, goal_update)
    sub3 = rospy.Subscriber('/lidar_topic_obj',Point, obj_update)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)

    speed = Twist()

    r = rospy.Rate(4)
    
    while not rospy.is_shutdown():
        
        #print(called)
        if flag2==1 and flag3 ==1 and update ==2 and called == 2:
            
            go_x = obj_loc[0] - goal_loc[0]
            go_y = obj_loc[1] - goal_loc[1]
            temp = ((go_x)**2+(go_y)**2)**0.5
            if(temp!=0):
                go_x=go_x/temp
                go_y=go_y/temp

            go_x = go_x*2
            go_y = go_y*2

            ex = Point()
            
            ex.x = obj_loc[0] + go_x
            ex.y = obj_loc[1] + go_y

            called=3
         
        if called == 3:
            inc_x = ex.x -x

            inc_y = ex.y -y

            angle_to_goal = atan2(inc_y, inc_x)

            if inc_x < 1 and inc_y < 1:
                flag3 = 0
                flag4 = 1
                speed.linear.x = 0.0
                speed.angular.z = 0.0
             
                called = 4
                #break
            elif abs(angle_to_goal - theta) > 0.5:
                speed.linear.x = 0.0
                speed.angular.z = 1.0
            else:
                if flag4 ==0:
                    speed.linear.x = 1.0
                    speed.angular.z = 0.0
                elif flag4 ==1:
                    speed.linear.x = 0.0
                    speed.angular.z = 0.0  
                    flag3 = 0  
                    flag4 = 2           
              
                
        if called == 4:
            print(called)
            flag3 =0
            
            time.sleep(0.5)
            if flag5 == 0:
                flag = 0
            else:
                flag = 1
            #speed.linear.x = 0.0
            #speed.angular.z = 0.0
            if flag5 ==0:
                angle_to_obj = atan2(obj_loc[1],obj_loc[0])
                #angle_to_obj = -angle_to_obj 
                flag5 = 1
            
            print('obj_loc', obj_loc)
            print('angle_to_obj', angle_to_obj)
            #time.sleep(1)
            #speed.linear.x = 0.0
            
            print('theta',theta)
            #print(angle_to_obj)
            if abs(angle_to_obj - theta) > 0.2:
                speed.linear.x = 0.0
                speed.angular.z = 0.5
            elif abs(angle_to_obj - theta) <= 0.2:
                speed.linear.x = 1.0
                speed.angular.z = 0.0
                called = 5
        
        if called == 5:
            flag3 = 0
            angle_to_obj = atan2(obj_loc[0],obj_loc[1])
            
            #flag = 0
            if abs(angle_to_obj) <= 0.5:
                flag3 = 0
                angle_to_obj = atan2(obj_loc[0],obj_loc[1])
                
            elif abs(angle_to_obj) > 0.5:
                flag2 = 0
                flag3 = 0
                flag = 0
                called = 2
            
        pub.publish(speed)
        r.sleep()  

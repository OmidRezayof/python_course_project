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

flag = 0
flag2=0
flag3=0
init_x = 0.0
init_y = 0.0 
init_theta = 0.0
x = 0
y = 0
theta = 0
goal_loc=[0,0]
obj_loc = [0,0]
called=0
#need to write another script to get the initial odometry and theta only once then
#subtract those values from the newOdom updating x and y 
#x and y need to be the odometry reading - the initial odometry reading when husky is asked to move to x
def goal_update(msg):
    global goal_loc,called
    global flag2
    if flag2 == 0:
        goal_loc[0] = msg.x
        print("test")
        goal_loc[1] = msg.y
        flag2 = 1
        called=called+1
def obj_update(msg):
    global obj_loc ,called
    global flag3
    if flag3 == 0:
            
        print("test2")
        obj_loc[0] = msg.x
        obj_loc[1] = msg.y
        flag3 = 1
        called=called+1
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
        
        print(called)
        if called==2:
            x_x = abs(goal_loc[0] - obj_loc[0])
            x_y = abs(goal_loc[1] - obj_loc[1])
            x_phi = tan(x_x/x_y)
            x_l = sqrt(x_x**2 + x_y**2) + 7
            #print('x_l',x_l)
            #print(x_theta)

            goal = Point()
            
            goal.x = x_l*sin(x_phi)
            #print(goal.x)
            #print(goal.x)
            goal.y = x_l*cos(x_phi)
            #print(goal.y)
            called=3
         
        elif called == 3:
            inc_x = goal.x -x
            print(inc_x)
            #print(inc_x)
        #print(x)
        #print('x', x)
            #print(goal.x)
            inc_y = goal.y -y
        #print('y', y)
        #print(inc_y)
            angle_to_goal = atan2(inc_y, inc_x)
            print('angle_to_goal', angle_to_goal)
            print('theta', theta)
        #print(angle_to_goal)
            if inc_x < 0.5 and inc_y < 0.5:
                speed.linear.x = 0.0
                speed.angular.z = 0.0
                break

   
        #print(angle_to_goal)

            elif abs(angle_to_goal - theta) > 0.5:
                speed.linear.x = 0.0
                speed.angular.z = 1.0
                print(speed.angular.z)
            else:
                speed.linear.x = 1.0
                speed.angular.z = 0.0

        pub.publish(speed)
        r.sleep()   
   

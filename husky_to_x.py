# -*- coding: utf-8 -*-
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
from math import tan
from math import sin
from math import cos

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
#need to write another script to get the initial odometry and theta only once then
#subtract those values from the newOdom updating x and y 
#x and y need to be the odometry reading - the initial odometry reading when husky is asked to move to x
def goal_update(msg):

    global goal_loc
    goal_loc[0] = msg.x
    print("test")
    goal_loc[1] = msg.y
def obj_update(msg):
    global obj_loc 
    print("test2")
    obj_loc[0] = msg.x
    obj_loc[1] = msg.y
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
        
rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
sub2 = rospy.Subscriber('/lidar_topic_goal',Point, goal_update)
sub3 = rospy.Subscriber('/lidar_topic_obj',Point, obj_update)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)

speed = Twist()

r = rospy.Rate(4)

x_x = goal_loc[0] - obj_loc[0]
x_y = goal_loc[1] - obj_loc[1]
x_theta = tan(x_x/x_y)
x_l = (x_x**2 + x_y**2) + 10

goal = Point()
goal.x = x_l*sin(x_theta)
goal.y = x_l*cos(x_theta)

while not rospy.is_shutdown():
    inc_x = goal.x -x
    inc_y = goal.y -y
    
    if inc_x < 0.5 and inc_y < 3:
        speed.linear.x = 0.0
        speed.angular.z = 0.0

    angle_to_goal = atan2(inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.1:
        speed.linear.x = 0.0
        speed.angular.z = 0.3
    else:
        speed.linear.x = 0.5
        speed.angular.z = 0.0

    pub.publish(speed)
    r.sleep()    

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

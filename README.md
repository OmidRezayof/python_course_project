# M E 396 P - Application Programming for Engineers
# Object Herding Simulation
## Group G11: Juliana Iverson , Austin Uresti , Omid Rezayof
_jiverson@utexas.edu / austinu@utexas.edu / omid.rezayof@utexas.edu_

## Package Prequisites

Our project depends on several external packages in order to work.

The following list covers the main packages used. Note that there may be other prequisite packages not already installed on your machine that will need to be installed per package instructions

All software was tested on [Ubuntu 20.04.06 Focal Fossa](https://releases.ubuntu.com/focal/)

The following links provide instructions on how to install the prequisite software and packages used in our project onto your computer

Package 1: [Robot Operating System Noetic (ROS)](http://wiki.ros.org/noetic/Installation/Ubuntu)

Package 2: [Gazebo 11](https://classic.gazebosim.org/tutorials?tut=install_ubuntu&cat=install)

Package 3: [RViz](http://wiki.ros.org/rviz/UserGuide)

    **IMPORTANT: MAKE SURE YOU INSTALL SOFTWARE FOR NOETIC ROS**

    i.e. `sudo apt-get install ros-noetic-rviz`

Package 4: [ClearPath Robotics Husky Desktop & Husky Simulator](https://www.clearpathrobotics.com/assets/guides/noetic/husky/DrivingHusky.html)

Package 5: [Catkin](http://wiki.ros.org/catkin#Installing_catkin)

Package 6: [ROS Joy](http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick)
## How To Run

**IMPORTANT: run `source /opt/ros/noetic/setup.bash` on any new terminal page you open before doing anything else
**

You will also need the following python modules to be installed to your python3 installation:

[Pygame](https://www.pygame.org/wiki/GettingStarted)
[numpy](https://numpy.org/install/)

1. For Gazebo simulation, please download our world file (_new_world2.world_) and place it in the 
`/opt/ros/noetic/share/husky_gazebo/worlds` directory. 
   _Note that depending on your user permissions, you may need to execute a sudo copy function in order to copy the file into a protected space_

   `$ sudo cp ~/Downloads/new_world_2.world ~/opt/ros/noetic/share/husky_gazebo/worlds` _

2. Create a catkin workspace, change to the catkin workspace directory, and create your containing package. 

   `$ mkdir -p ~/catkin_ws/src`

   `$ cd ~/catkin_ws/src`

   `$ catkin_create_pkg your_package std_msgs rospy geometry_msgs`

(For more details on creating a workspace, see the following links: 
http://wiki.ros.org/catkin/Tutorials/create_a_workspace & http://wiki.ros.org/ROS/Tutorials/CreatingPackage)

5. Clone our repository to your local machine

   `$ git clone https://github.com/OmidRezayof/python_course_project ~/catkin_ws/src/your_package/src`
   
   or alternatively download all the .py files and place them into the src folder inside your custom package.

7. Return to the catkin workspace directory and run the catkin make function. This compiles the package.

   `$ cd ~/catkin_ws/src`

   `$ catkin_make`

8. Your package should now be ready for use.


### Pygame Visualization


First start with running roscore. In a new terminal page type:

`roscore`

On a new terminal page type:

`rosrun joy joy_node`

This will run the joy_node node which is for communicating with Xbox controller. 

On a new terminal, create a directory for our project and pull our repository. After that, cd to the directory and run:

`python3 goal_loc & python3 dog_loc & python3 obj_loc & python3 pygame_node`

You can use the right thumbstick to move the goal and the left thumbstick to give disturbances to the object. 

### Gazebo Visualization

#### Starting Simulation

Open a new terminal window and run:

`source /opt/ros/noetic/setup.bash`

`export HUSKY_LMS1XX_ENABLED=1`

`roslaunch husky_gazebo husky_newworld.launch`

#### Viewing LiDAR & other Robot Vitals

`source /opt/ros/noetic/setup.bash`

`roslaunch husky_viz view_robot.launch`

#### Launching Python Code

To run the "husky_to_x.py", first cd to your_package/src and then run:

`python3 scan.py & python3 husky_to_x.py`

To run the moving cylinder simulation, after opening gazebo, cd to your package's src directory and run:

`python3 comnew.py`

and on a new terminal page, publish a message like this in order to move the cylinder:

`rostopic pub -r 10 /cylinder_velocity geometry_msgs/Twist  '{linear:  {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'`


This is the link to our presentation, you can find more information on how you can control and play with this objects:

https://docs.google.com/presentation/d/17h3HP_62Bj14_MxYqViFvrI0khu8-iKaYJdJY8pVOmc/edit?usp=sharing


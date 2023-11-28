# python_course_project
ROSstress4less

Repo for course project

This is a repository for our group project on python programming course. 
Group: G11 / members: Juliana Iverson, Austin Uresti, Omid Rezayof

## Quick tip on installing gazebo / husky

%% BY AUSTIN %%


## How To Run
To run this project, you will need to have ROS (noetic) up and running on your ubuntu. 

You will also need these packages to be installed:

Pygame, Numpy, Joy (within ROS environment), catkin

You will need Gazebo and Husky (within Gazebo) installed for the Gazebo simulation. 
For Gazebo simulation, please download our world file (.world) and put it in the 
`/opt/ros/noetic/share/husky_gazebo/worlds`
directory. 

start by creating a catkin workspace, and a desired package (for looking into how to create catkin workspace and packages look at: 
`http://wiki.ros.org/catkin/Tutorials/create_a_workspace` & `http://wiki.ros.org/ROS/Tutorials/CreatingPackage`)

then pull our repository our download all the .py files into the src folder inside your custom package)

**IMPORTANT: run `source /opt/ros/noetic/setup.bash` on any new terminal page you open before doing anything else**

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


Open a new terminal window and run:

`roslaunch husky_gazebo husky_playpen.launch`

To run the simulation with a joystick, open a new terminal and run:

`rosrun joy joy_node`

%%% BY AUSTIN%%%

To run the "husky_to_x.py", first cd to your_package/src and then run:
`python3 scan.py & python3 husky_to_x.py`

To run the moving cylinder simulation, after opening gazebo, cd to your package's src directory and run:

`python3 comnew.py`

and on a new terminal page, publish a message like this:

`rostopic pub -r 10 /cylinder_velocity geometry_msgs/Twist  '{linear:  {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'`


This is the link to our presentation, you can find more information on how you can control and play with this objects:

https://docs.google.com/presentation/d/17h3HP_62Bj14_MxYqViFvrI0khu8-iKaYJdJY8pVOmc/edit?usp=sharing


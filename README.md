# python_course_project
Repo for course project

This is a repository for our group project on python programming course. 
Group: G11 / members: Juliana Iverson, Austin Uresti, Omid Rezayof


The structure of the project will come in later lines:
ROSCORE - Central Communication Hub

nodes:

  obj_loc_node

  spot_loc_node
  
  goal_loc_node
  
  joy_node
  
  pygame_node

## How To Run
To run this project, you will need to have ROS (noetic) up and running on your ubuntu. 

You will also need these packages to be installed:

Pygame, Numpy, Joy (within ROS environment)

First start with running roscore. In a new terminal page type:
`roscore`


On a new terminal page type:
`rosrun joy joy_node`

This will run the joy_node node which is for communicating with Xbox controller. 


On a new terminal, create a directory for our project and pull our repository. After that, cd to the directory and run:

`python3 goal_loc & python3 spot_loc & python3 obj_loc & python3 pygame_node`



further description about the project can be found here:
https://docs.google.com/document/d/1AMOzLVFcYRZKSjEhWGjXj2QBbK9PRXhLxicLFOlFrj4/edit


## Flytbase Assisment
### Created by: - Ramprasad Anand Kulkarni



**setting up the development environment**
1) Install ros noetic desktop

`http://wiki.ros.org/noetic/Installation/Ubuntu`

2) Create local workspace 

`mkdir -p catkin_ws/src && cd catkin_ws`

3) Build the workspace

`catkin_make`

4) Clone the repository

` git clone https://github.com/21coolkarni/Flytbase_assisment.git`

5) Copy and pase the turtle package folder to `catkin_ws/src`

6) Build the workspace 

`catkin_make`

7) Source the workspace 

`source devel/setup.bash`

8) Open another terminal and run roscore

`roscore`

9) Run turtlesim node 

`rosrun turtlesim turtlesim_node`

10) Open code from the directory `catkin_ws/src/turtle/scripts` and find `def main()` which contains the commented testcase functions, un-comment the testcase functions as per the requirement and run the code

11) Run the code using 

`rosrun turtle assisment.py`

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

10) Run the code using 

`rosrun turtle assisment.py`

11) Enter your testcase choice from 1 to 5 to run the specific testcase



## **Case 1**

**Algorithm:** 
- Find Euclidian distance from the current point to the desigred point and calculate the speed by multiplying it with a constant p value, as the distance decreases speed decreases and eventually becomes zero.
- Find Desigred angle by using a tan2 function which gives the angle of the disired goal and multiply it with a constant p value, as the angle decreases turning speed decreases and eventually becomes zero.
- Publish these values with twist msgs.
- Accept a certain ammount of error while reaching the distance to avoid infinite loop.

**Output:**
<p align="center">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236546205-89a8ddae-61f3-4b78-9bdb-0a1278a67ff8.png">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236546305-3b20c88c-2653-4bfb-b305-17c4130dfdcd.png">
</p>

## **Case 2**

**Algorithm:**
- Spawn the turtle at the start of the grid position. 
- Rotate and move functions will move the turtle into desired grid.
- Turtle will accelerate till it reaches the mid point of the total distance and then it will decelerate again it reaches the final destination
 
**Output:**

<p align="center">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547103-e98e719e-0665-4c0f-86d5-62be10d51493.png">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547153-45c74420-4be9-49a4-823a-af8028a4e636.png">
</p>

## **Case 3**

**Algorithm:**
- Spwn the turtle at a position which is suitable for drawing the circle.
- Using circle position publish twist msgs which publishes the twist msgs with linear.x as radius and angular,z as speed.
- **Multithreading :** Create a timer object with rosspy duration of 5 seconds to publish /rt_real_pose and tr_noisy_pose msgs
 
**Output:**

<p align="center">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547515-5c4b23ad-1d0e-4570-8b74-aa4f9e5ffd9a.png">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547530-283e5df9-4359-4790-b88f-fb32cde2f4fb.png">
</p>

## **Case 4**

**Algorithm:**

**Multithreading :** Create a timer object with very short rospy duration for controlling the police turtle to chase down the robber turtle with fast speed.
- Fast_pt_publisher function will spawn the police turtle after 10 seconds with pt_spawn_bool tag
- Then it will subscribe to the /rt_real_pose msgs
- Then after getting the position of the thief police turtle will catch the thief with '/rt_real_pose' with faster speed than robber turtle

**Output:**

<p align="center">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547910-f6858835-7d56-4561-b8e6-2b3aa157dc0e.png">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547914-007a3b94-edd7-480c-9d0e-a7a420e55264.png">
</p>

## **Case 5**

**Algorithm:**
- Algorithm is similar to case4 but this time speed of the turtle is slow so we need to predict the future co-ordinates of the turtle where its going to be at perticular point of time after getting its perticular location and then reach on that position before the robber turtle to catch it
- We will use predict function which will give the future predicted points of the robber turtle and then use slow_pt_publisher funciton to reach at that perticular location with slower speed than 
- First of all go to the center of the turtle window as every point on the turtle window is at equal distance from the center position
- Then record the 3 positions of the robber turtle within 15 seconds
- Calculate the center of the circle and radius of the circle in which the robber turtle is rotating 
- Wait for the new '/rt_real_pose' msgs and as soon as the msg arrives calculate the theta of the predicted position of the turtle using atan2 function and then add a constant theta value to the desigred theta which will compensate for slow speed 
- Go to the predicted position and catch the thief

**Output:**

<p align="center">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547989-f178719d-744c-4206-aa32-71415489cc44.png">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236547993-6d7bde58-7c73-4657-bdcc-5d023b925731.png">
</p>


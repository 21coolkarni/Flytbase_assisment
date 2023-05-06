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
- Find Euclidian distance from the current point to the desigred point and calculate the speed by multiplying it with a constant p value, as the distance decreases speed decreases and eventually becomes zero
- Find Desigred angle by using a tan2 function which gives the angle of the disired goal and multiply it with a constant p value, as the angle decreases turning speed decreases and eventually becomes zero 
- Publish these values with twist msgs
- Accept a certain ammount of error while reaching the distance to avoid infinite loop
- Output:
<p align="center">
<img width="50%" src ="https://user-images.githubusercontent.com/84247246/236546205-89a8ddae-61f3-4b78-9bdb-0a1278a67ff8.png">
![Screenshot from 2023-05-06 00-16-25](https://user-images.githubusercontent.com/84247246/236546305-3b20c88c-2653-4bfb-b305-17c4130dfdcd.png)
</p>

**Case 2**

![Screenshot from 2023-05-06 00-21-18](https://user-images.githubusercontent.com/84247246/236547103-e98e719e-0665-4c0f-86d5-62be10d51493.png)
![Screenshot from 2023-05-06 00-20-50](https://user-images.githubusercontent.com/84247246/236547153-45c74420-4be9-49a4-823a-af8028a4e636.png)

**Case 3**

![Screenshot from 2023-05-06 00-21-46](https://user-images.githubusercontent.com/84247246/236547515-5c4b23ad-1d0e-4570-8b74-aa4f9e5ffd9a.png)
![Screenshot from 2023-05-06 00-22-18](https://user-images.githubusercontent.com/84247246/236547530-283e5df9-4359-4790-b88f-fb32cde2f4fb.png)


**Case 4**

![Screenshot from 2023-05-06 00-23-50](https://user-images.githubusercontent.com/84247246/236547910-f6858835-7d56-4561-b8e6-2b3aa157dc0e.png)
![Screenshot from 2023-05-06 00-23-55](https://user-images.githubusercontent.com/84247246/236547914-007a3b94-edd7-480c-9d0e-a7a420e55264.png)

**Case 5**

![Screenshot from 2023-05-06 00-25-25](https://user-images.githubusercontent.com/84247246/236547989-f178719d-744c-4206-aa32-71415489cc44.png)
![Screenshot from 2023-05-06 00-25-43](https://user-images.githubusercontent.com/84247246/236547993-6d7bde58-7c73-4657-bdcc-5d023b925731.png)

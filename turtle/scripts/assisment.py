# Created by :- Ramprasad Anand Kulkarni
# gmail :- 21coolkarni@gmail.com


# importing packages
#--------------------------------------------------------------------------------------------------------------------------------------------------#

import rospy
from turtlesim.srv import Kill, Spawn
import random
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
from turtle.PrintColours import *
import threading
import numpy as np

# Global veraibles
#--------------------------------------------------------------------------------------------------------------------------------------------------# 

v_msg = Twist()             # Object for twist msgs
lock = threading.Lock()     # Object for threadlock used for 
PI = 3.1415926535897        # Default pi value
pt_spawn_bool = False       # Flag to check if the police turtle is spawned or not
thief_captured = False      # Flag to check is the thief is captured or not
radius = 0.5                # Default value for radius of the circle 
speed = 0.1                 # Default valur for speed of the circle 


# Publishers for publishing the msgs
#--------------------------------------------------------------------------------------------------------------------------------------------------# 


realPose_pub = rospy.Publisher('/rt_real_pose',Pose,queue_size=5)        # Publisher for publishing the real pose of the thief turtle

noisePose_pub = rospy.Publisher('/rt_noisy_pose',Pose,queue_size=5)      # Publisher for publishing the noisy pose of the thief turtle

pcontrol_pub = rospy.Publisher('/pturtle/cmd_vel',Twist,queue_size=5)    # Publisher for controlling the police turtle

control_pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size = 5)   # Publisher for controlling the thief turtle


# Publishing the /rt_real_pose /rt_noisy_pose msgs
#--------------------------------------------------------------------------------------------------------------------------------------------------# 

def publish_msgs(event):
    
    lock.acquire()                                                       # Aquiring data lock before accessing and writing the data 
    global x,y,z
    pose_rmsg = rospy.wait_for_message('/turtle1/pose', Pose)
    rmsg = Pose()
    rmsg.x = pose_rmsg.x
    rmsg.y = pose_rmsg.y
    rmsg.theta = pose_rmsg.theta
    rmsg.linear_velocity = pose_rmsg.linear_velocity
    rmsg.angular_velocity = pose_rmsg.angular_velocity
    realPose_pub.publish(rmsg)
    
    noise = random.randrange(-10,10,1)
    pose_nmsg = rospy.wait_for_message('/turtle1/pose', Pose)
    nmsg = Pose()
    nmsg.x = pose_nmsg.x + noise
    nmsg.y = pose_nmsg.y + noise
    nmsg.theta = pose_nmsg.theta + noise
    nmsg.linear_velocity = pose_nmsg.linear_velocity + noise
    nmsg.angular_velocity = pose_nmsg.angular_velocity + noise
    
    noisePose_pub.publish(nmsg)
    
    lock.release()                                                       # Releasing the lock
    

# Function to case down the turtle with slow speed 
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def slow_pt_publisher(event):
    global pt_spawn_bool,rx,ry,rz
    if not pt_spawn_bool:                                                # Checking if the police turtle is spawned or not  
        rospy.sleep(10.)                                                 # Sleep for 10 min before spawning
        spawn_pt()                                                       # Spawning the Police turtle 
        pt_center_reach(5.5,5.5)                                         # Reach center of the frame
        pt_spawn_bool = True
    pose_msg = rospy.wait_for_message('/rt_real_pose', Pose)             # Wait for the first msg to initialize the x,y,z veriables
    rx = pose_msg.x
    ry = pose_msg.y
    if not thief_captured:                                               # Checking if the thief is captured or not 
        pred_x,pred_y = pose_prediction()                                # Get the predicted values of the turtle from the function pose_prediction
        reach_thief_slow(pred_x,pred_y)                                  # Reach at the predicted location with slow speed


# Function to case down the turtle with fast speed
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def fast_pt_publisher(event):
    
    global pt_spawn_bool,rx,ry,rz                                         
    if not pt_spawn_bool:                                                # Checking if the police turtle is spawned or not 
        rospy.sleep(10.)
        spawn_pt()
        pt_spawn_bool = True
        
    pose_msg = rospy.wait_for_message('/rt_real_pose', Pose)             # Wait for the first msg to initialize the x,y,z veriables
    rx = pose_msg.x
    ry = pose_msg.y
    if not thief_captured:
        reach_thief_fast(rx,ry)
        

#Callback functions for Subscribers 
#--------------------------------------------------------------------------------------------------------------------------------------------------# 


def rt_real_pose_cb(msg):                                                #Callback for /rt_real_pose topic subscriber 
    
    global rx,ry,rz
    rx = msg.x
    ry = msg.y
    rz = msg.theta
    
def pturtle_pose_cb(msg):                                                #Callback for /pturtle/pose topic subscriber 
    
    global px,py,pz
    px = msg.x
    py = msg.y
    pz = msg.theta
    
def pose_cb(msg):                                                        #Callback for /turtle1/pose topic subscriber 
     
    global x,y,z
    x = msg.x
    y = msg.y
    z = msg.theta
    
    
# function for finding the center point(x,y) and the redius of the circle 
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def define_circle(p1, p2, p3):
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    
    if abs(det) < 1.0e-6:
        return (None, np.inf)
    
    
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det                # Finding x co-cordinate of the center of the circle
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det            # Finding y co-cordinate of the center of the circle
    
    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)                 # Finding radius with Euclidean distance
    return ((cx, cy), radius)                                           # Returning x,y,co-cordinates and radius


# function for finding the center point(x,y) and the redius of the circle 
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def distance(p1, p2, p3, p4):                           
    return abs(math.sqrt((p1 - p2)**2 + (p3 - p4)**2))                  # Returning the Euclidean distance with formula


# function for predicting the future position of the thief turtle rotating in circles used when police turtle speed is slower than thief turtle
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def pose_prediction():
    
    global x,y,z
    pose_msg = rospy.wait_for_message('/turtle1/pose', Pose)            # wait for a msg from topic /turtle1/pose and store it      
    x = pose_msg.x
    y = pose_msg.y
    z = pose_msg.theta
    point1 = x,y,z                                                      # Saving postion of the first point
    rospy.sleep(5.)                                                     # Sleep for 5 seconds as /turtle1/pose is publishing every 5 seconds
    
    pose_msg = rospy.wait_for_message('/turtle1/pose', Pose)            
    x = pose_msg.x
    y = pose_msg.y
    z = pose_msg.theta
    point2 = x,y,z                                                      # Saving postion of the second point
    rospy.sleep(5.)  
                                                    
    pose_msg = rospy.wait_for_message('/turtle1/pose', Pose)
    x = pose_msg.x
    y = pose_msg.y
    z = pose_msg.theta
    point3 = x,y,z                                                      # Saving postion of the second point
    
    (cx, cy), radius = define_circle(point1,point2,point3)              # Getting position of the center point and radius of the circle 
     
    pose_msg = rospy.wait_for_message('/turtle1/pose', Pose)            # Fanally gatting the position of the thief turtle one more time to chase is down
    x = pose_msg.x
    y = pose_msg.y
    z = pose_msg.theta
    
    current_angle = math.atan2(y-cy,x-cx)                               # Finding the angle of current position of the thief turtle   
    angle = current_angle + math.radians(220)                           # Addning a calibrated angle to the final destination's angle at which the thief turtle is going to be with the current speed
    fx = radius * math.cos(angle) + cx                                  # Formule for finding the x point on a circumference of a circle when radius, theta, center co-ordinates are given 
    fy = radius * math.sin(angle) + cy                                  # Formule for finding the y point on a circumference of a circle when radius, theta, center co-ordinates are given                
    return fx,fy                                                        # Return the final fx,fy predicted co-ordinates of the thief


# Spawning functions for police and thief turtle
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def random_spawn():                                                     # Spawn theif turtle at random position

    x_new= round(random.uniform(0,11), 4)
    y_new = round(random.uniform(0,11), 4)
    z_new = random.randint(0,360)
    rospy.wait_for_service('/kill')
    delete = rospy.ServiceProxy('/kill',Kill)
    delete('turtle1')
    rospy.wait_for_service('/spawn')
    spawn = rospy.ServiceProxy('/spawn',Spawn)
    spawn(x_new,y_new,z_new,'turtle1')

def spawn_pt():                                                         # Spawn police turtle at random position
    
    x_new= round(random.uniform(0,11), 4)
    y_new = round(random.uniform(0,11), 4)
    z_new = random.randint(0,360)
    try:
        rospy.wait_for_service('/kill')
        delete = rospy.ServiceProxy('/kill',Kill)
        delete('pturtle')
    except:
        pass
    rospy.wait_for_service('/spawn')
    spawn = rospy.ServiceProxy('/spawn',Spawn)
    spawn(x_new,y_new,z_new,'pturtle')

def start_spawn():                                                      # Spawn the thief turtle at the start of the grid 
    
    rospy.wait_for_service('/kill')
    delete = rospy.ServiceProxy('/kill',Kill)
    delete('turtle1')
    rospy.wait_for_service('/spawn')
    spawn = rospy.ServiceProxy('/spawn',Spawn)
    spawn(1,1,0,'turtle1')
    
def cir_spawn():                                                        # Spawn the thief turtle at position which is suitable for drawing a large circle
    
    rospy.wait_for_service('/kill')
    delete = rospy.ServiceProxy('/kill',Kill)
    delete('turtle1')
    rospy.wait_for_service('/spawn')
    spawn = rospy.ServiceProxy('/spawn',Spawn)
    spawn(5.5,1,0,'turtle1')
    
def mid_spawn():                                                        # Spawn the thief turtle at middle position of the frame   
    
    rospy.wait_for_service('/kill')
    delete = rospy.ServiceProxy('/kill',Kill)
    delete('turtle1')
    rospy.wait_for_service('/spawn')
    spawn = rospy.ServiceProxy('/spawn',Spawn)
    spawn(5.5,5.5,0,'turtle1')
    

# function to move the turtle when direction and distance is given    
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def move(distance,is_forward):                                          
    
    global x,y,z
    pose_msg = rospy.wait_for_message('/turtle1/pose', Pose)            # Wait for a msg from topic /turtle1/pose and store it
    x = pose_msg.x
    y = pose_msg.y
    z = pose_msg.theta
    x0=x                                                                # Saving the initial position of the turtle in x0 and y0
    y0=y
    speed = 2

    if (is_forward):                                                    # If the direction is forward then move in forward direction 
            v_msg.linear.x =abs(speed)
    else:                                                               # If the direction is backward then move in backward direction 
        v_msg.linear.x =-abs(speed)                                       
        
    distance_moved = 0.0                                                # Veriable to store the distance
    loop_rate = rospy.Rate(10)
    while not rospy.is_shutdown() :                                     # while loop to keep moving in that direction
                if distance_moved<distance/2:                           # If the travelled distance is lesser than complete distance then accelerate 
                    v_msg.linear.x += 0.5                               # Accelerating with 0.5 factor
                    rospy.loginfo(CBOLD + CGREEN2 + "Accelerating" + CEND)
                    
                elif distance_moved>distance/2:                         # If the travelled distance is grater than complete distance then decelerate
                    v_msg.linear.x -= 0.5                               # Decelerate with 0.5 factor 
                    rospy.loginfo(CBOLD + CRED2 + "Breaking" + CEND)
                    
                control_pub.publish(v_msg)  
                loop_rate.sleep()
                distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2))) #Calulating Euclidean distance
                              
                if  not (distance_moved<distance):                      # If total distance travelled becomes negative or zero break the loop 
                    rospy.loginfo(CBOLD + CGREEN2 + "Reached" + CEND)
                    break
        
    v_msg.linear.x =0                                                   # Forecefully stop the turtle by publishing the stop msgs
    control_pub.publish(v_msg)


# Function to rotate the turtle when the angle of rotation and direction of the ratation
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def rotate(angle,rotation):
    speed = 15
    rate = rospy.Rate(10)
    v_msg.linear.x=0
    v_msg.linear.y=0
    v_msg.linear.z=0
    v_msg.angular.x=0
    v_msg.angular.y=0
    angular_speed = speed*2*PI/360                                      # Changing angular speed from degree per second to radians per second 
    relative_angle = angle*2*PI/360                                     # Changing relative speed from degree per second to radians per second 
    if rotation:                                                        # Checking if the rotation is anti-clockwise or clockwise
        v_msg.angular.z = -abs(angular_speed)
    else:
        v_msg.angular.z = abs(angular_speed)
    # Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()                                      # Time veraible to keep track of the degrees moved
    current_angle = 0
    while(current_angle + 0.05 < relative_angle):                       # wihle loop to rotate with 0.05 error compensating factor. If current angle is lesser than final angle then enter the while loop
        control_pub.publish(v_msg)                                      
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)                           # Current angle calculation
        rate.sleep()                                                    
        rospy.loginfo(CBLUE2 + "Rotating" + CEND)
    v_msg.angular.z = 0                                                 # Forcefully stop rotating when angle is reached
    control_pub.publish(v_msg)
    
    
# Function to rotate the turtle in circular motion when radius and speed is given  
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def circle(radius,speed):
    rate = rospy.Rate(10)
    timer = rospy.Timer(rospy.Duration(5), publish_msgs)
    rospy.loginfo(CBLUE2 + "Moving in circles" + CEND)
    while not rospy.is_shutdown() and not thief_captured:
        v_msg.linear.x = radius
        v_msg.linear.y = 0
        v_msg.linear.z = 0
        v_msg.angular.x = 0
        v_msg.angular.y = 0
        v_msg.angular.z = speed
        
        control_pub.publish(v_msg)
        rate.sleep()
        
        
# Function to reach a goal Position when x and y co-ordinates of the point are given
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def reach_goal(goalx,goaly):
    global x,y,z
    pose_msg = rospy.wait_for_message('/turtle1/pose', Pose)
    x = pose_msg.x
    y = pose_msg.y
    z = pose_msg.theta
    rate = rospy.Rate(10)
    rospy.loginfo(CBLUE2 + "Reaching goal x = 5.5,y = 5.5" + CEND)
    while not rospy.is_shutdown() and True:

        p_gainv = 0.8                                                       # P value of the PID loop which will control the correction of the velocity error

        dist = abs(math.sqrt(((goalx-x)**2)+((goaly-y)**2)))                # Equlidian Distance to find toal distance
        speed = dist * p_gainv                                              # As the distance decreases speed will decrease and eventually zero 

        p_gaina = 3.6                                                       # P value of the PID loop which will control the correction of the angular error                                                

        desired_angle_goal = math.atan2(goaly-y,goalx-x)                    # Finding desired angle with atan2 
        angular_speed = (desired_angle_goal-z) * p_gaina                    # As the angle decreases angular speed will decrease and eventually zero

        v_msg.linear.x = speed
        v_msg.angular.z = angular_speed
        control_pub.publish(v_msg)
        rate.sleep()

        if dist < 0.1:                                                      # Fine error margin to reach at that distance to avoid infinite loops 
            rospy.loginfo(CBOLD + CGREEN2 + "Goal Reached" + CEND)
            break


# Function for police turtle to reach the center of the frame
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def pt_center_reach(goalx,goaly):
    
    global px,py,pz
    pose_msg = rospy.wait_for_message('/pturtle/pose', Pose)
    px = pose_msg.x
    py = pose_msg.y
    pz = pose_msg.theta
    rate = rospy.Rate(10)
    rospy.loginfo(CBLUE2 + "Reaching Center" + CEND)
    while not rospy.is_shutdown() and True:

        p_gainv = 0.8

        dist = abs(math.sqrt(((goalx-px)**2)+((goaly-py)**2)))
        speed = dist * p_gainv

        p_gaina = 4

        desired_angle_goal = math.atan2(goaly-py,goalx-px)
        angular_speed = (desired_angle_goal-pz) * p_gaina

        v_msg.linear.x = speed
        v_msg.angular.z = angular_speed
        pcontrol_pub.publish(v_msg)
        rate.sleep()

        if dist < 0.1:
            rospy.loginfo(CBOLD + CGREEN2 + "Center Reached" + CEND)
            break
        
        
# Function for police turtle to catch the thief turtle with slow speed
#--------------------------------------------------------------------------------------------------------------------------------------------------#


def reach_thief_slow(goalx,goaly):
    distance1 = 0
    global px,py,pz,thief_captured
    pose_msg = rospy.wait_for_message('/pturtle/pose', Pose)
    px = pose_msg.x
    py = pose_msg.y
    pz = pose_msg.theta
    rate = rospy.Rate(10)
    rospy.loginfo(CBLUE2 + "Trying to catch thief" + CEND)
    while not rospy.is_shutdown() and not thief_captured:

        p_gainv = 0.8
        dist = abs(math.sqrt(((goalx-px)**2)+((goaly-py)**2)))
        speed = dist * p_gainv

        p_gaina = 3.2

        desired_angle_goal = math.atan2(goaly-py,goalx-px)
        angular_speed = (desired_angle_goal-pz) * p_gaina

        v_msg.linear.x = speed
        v_msg.angular.z = angular_speed
        pcontrol_pub.publish(v_msg)
        rate.sleep()
        distance1 = distance(px,x,py,y)
        
        if distance1 < 3:
            rospy.loginfo(CBOLD + CGREEN2 + "Thief Captured !!!!!" + CEND)
            thief_captured = True
            break


# Function for police turtle to catch the thief with fast speed
#--------------------------------------------------------------------------------------------------------------------------------------------------# 

    
def reach_thief_fast(goalx,goaly):
    distance1 = 0
    global px,py,pz,thief_captured
    pose_msg = rospy.wait_for_message('/pturtle/pose', Pose)
    px = pose_msg.x
    py = pose_msg.y
    pz = pose_msg.theta
    rate = rospy.Rate(10)
    rospy.loginfo(CBLUE2 + "Trying to catch thief" + CEND)
    while not rospy.is_shutdown() and not thief_captured:

        p_gainv = 1
        dist = abs(math.sqrt(((goalx-px)**2)+((goaly-py)**2)))
        speed = dist * p_gainv
        
        p_gaina = 4

        desired_angle_goal = math.atan2(goaly-py,goalx-px)
        angular_speed = (desired_angle_goal-pz) * p_gaina

        v_msg.linear.x = speed
        v_msg.angular.z = angular_speed
        pcontrol_pub.publish(v_msg)
        rate.sleep()
        
        distance1 = distance(px,x,py,y)
        
        if distance1 < 3:
            rospy.loginfo(CBOLD + CGREEN2 + "Thief Captured !!!!!" + CEND)
            thief_captured = True
            break
# Test cases
#--------------------------------------------------------------------------------------------------------------------------------------------------# 


def case1():                                                                
    random_spawn()
    reach_goal(5.5,5.5)
    
    
def case2():
    start_spawn()
    time.sleep(1)
    rate = rospy.Rate(10)
    move(9.0,1)
    rate.sleep()
    rotate(90,0)
    rate.sleep()
    move(9.0,1)
    rate.sleep()
    rotate(90,0)
    rate.sleep()
    move(2.0,1)
    rate.sleep()
    rotate(90,0)
    rate.sleep()
    move(9.0,1)
    rate.sleep()
    rotate(90,1)
    rate.sleep()
    move(2.0,1)
    rate.sleep()
    rotate(90,1)
    rate.sleep()
    move(9.0,1)
    rate.sleep()
    rotate(90,0)
    rate.sleep()
    move(2.0,1)
    rate.sleep()
    rotate(90,0)
    rate.sleep()
    move(9.0,1)
    rate.sleep()
    rotate(90,1)
    rate.sleep()
    move(2.0,1)
    rate.sleep()
    rotate(90,1)
    rate.sleep()
    move(9.0,1)
    rate.sleep()

def case3(radius,speed):
    cir_spawn()
    # radius = int(input('Enter radius for the circle'))
    # speed = int(input('Enter speed for the circle'))
    circle(radius,speed)
    

def case4():
    
    timer2 = rospy.Timer(rospy.Duration(0.0001),fast_pt_publisher)
    case3(radius,speed)

def case5(radius,speed):
    timer3 = rospy.Timer(rospy.Duration(0.0001),slow_pt_publisher)
    case3(radius,speed)

def main():
    
    rospy.init_node('turtlebot_move')

    rospy.Subscriber('/turtle1/pose',Pose,pose_cb)
    
    rospy.Subscriber('/pturtle/pose',Pose,pturtle_pose_cb)
    
    rospy.Subscriber('/rt_real_pose',Pose,rt_real_pose_cb)
    
    time.sleep(1)

    choice = int(input('Enter the number for the testcase choises are 1, 2, 3, 4, 5 : '))
    
    if choice == 1:
        case1()
    elif choice == 2:
        case2()
    elif choice == 3:
        case3(5,1)
    elif choice == 4:
        case4()
    elif choice == 5:
        case5(5,1)
    else:
        print('Invalid choise')
    rospy.spin()

if __name__ == '__main__':
    main()  

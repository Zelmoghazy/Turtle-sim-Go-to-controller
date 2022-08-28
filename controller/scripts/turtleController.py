#!/usr/bin/env
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt

class Turtle:
    def __init__(self):
        rospy.init_node('turtle_controller',anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose,self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self,data):
        self.pose = data
        self.pose.x = round(self.pose.x,4)
        self.pose.y = round(self.pose.y,4)

    def distance(self,goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))

    def linear_velocity(self, goal_pose, vel_constant=rospy.get_param("/beta")):
        return vel_constant * self.distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_velocity(self, goal_pose, angle_constant=rospy.get_param("/phi")):
        return angle_constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move(self):
        
        choice = input("to enter new coordinates press y")
        if (choice == 'y'):
            if rospy.has_param('x_coordinate'):
                rospy.delete_param('x_coordinate')
            new = float(input ("enter x : "))    
            rospy.set_param('x_coordinate',new)
            if rospy.has_param('y_coordinate'):
                rospy.delete_param('y_coordinate')
            new = float(input ("enter y : "))    
            rospy.set_param('y_coordinate',new)

        goal_pose = Pose()
        goal_pose.x = rospy.get_param("/x_coordinate")
        goal_pose.y = rospy.get_param("/y_coordinate")

        vel_msg = Twist()

        while self.distance(goal_pose) >= 0.1:
            vel_msg.linear.x = self.linear_velocity(goal_pose)
            vel_msg.angular.z = self.angular_velocity(goal_pose)
            vel_msg.linear.y = 0 
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0   
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        
        print("Arrived")    
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.spin()
   
if __name__ == '__main__':
    try:
        x = Turtle()
        x.move()
    except rospy.ROSInterruptException:
        pass                









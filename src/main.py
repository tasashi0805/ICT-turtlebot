#!/usr/bin/env python 


import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64
from sensor_msgs.msg import Image, CameraInfo, CompressedImage, LaserScan
import sys
import math

class main:
    def __init__(self):
        print('init')
        self.sub = rospy.Subscriber('scan', LaserScan, self.laserScanCallback)  # define subscriber with name "scan"
        self.colorsub= rospy.Subscriber("color",String, self.col_msg_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        #self.msg_pub= rospy.Publisher("drive", Float64, queue_size=1)


        self.D_MAX = 1     # MAX_OBSTACLE_DISTANCE detection

        self.LV_MIN = 0.1    # MIN_LINEAR_VELOCITY
        self.LV_MAX = 2.6     # MAX_LINEAR_VELOCITY

        self.AV_MIN = 0.3     # MAX_ANGULAR_VELOCITY
        self.AV_MAX = 1.82     # MAX_ANGULAR_VELOCITY
        self.AV_FACTOR = 0.3    # adjuest performance

        self.DEFAULT_LV = 0.2   # DEFAULT_LINEAR_VELOCITY
        self.DEFAULT_AV = 0.0    # DEFAULT_ANGULAR_VELOCITY
        self.cloest_obtacle_distance = 1000   #ininiate cloest_obtacle_distance
        
        
        self.twist = Twist()

    def col_msg_callback(self,msg):
        data=msg.data
        if data=="blue":
            self.twist.linear.x=0.4
        elif data=="green":
            self.twist.linear.x=0.1
        elif data=="red":
            self.twist.linear.x=0
            print("Speed:",self.twist.linear)
            self.cmd_vel_pub.publish(self.twist)

        elif data=="No":
            self.twist.linear.x=0.2
        print("Speed:",self.twist.linear)
        self.cmd_vel_pub.publish(self.twist)


    # Input:
    #   msg: Data returned from callback function
    # Output:
    #   AV: New bot angular velocity
    def laserScanCallback(self, msg):
        self.twist.linear.x = self.DEFAULT_LV
        self.twist.angular.z = self.DEFAULT_AV

        sys.stdout.write('.') # write dots
        sys.stdout.flush()

        cloest_obtacle_distance = self.D_MAX
        cloest_obtacle_angle = 0

        # All beams used for detecting obstacles with difference of 5 degree (except the back one)
        for angle in range(-175, 175, 5):
            distance = round(msg.ranges[angle], 4)    # Distance to any obstacle along the current beam. Infinit if no obstacle was found
            if distance < cloest_obtacle_distance:     # If found any obstacle
                cloest_obtacle_distance = distance
                cloest_obtacle_angle = angle

        if cloest_obtacle_distance < self.D_MAX:     # If found any obstacle
            LV = 0.5
            AV = self.DEFAULT_AV
            d = cloest_obtacle_distance
            angle = cloest_obtacle_angle
            print()
            print('FOUND CLOSET OBSTACLE!! Distance:' + str(d) + ', Angle:' + str(angle) + ', Linear Velocity:' + str(LV) + ', Angular Velocity:' + str(AV))

            if angle >= 0 and angle < 90:
                LV = self.getLinearVelocity(d, LV, angle)
                AV = 0 - self.getAngularVelocity(d, angle)
            elif angle >= 90 and angle < 180:
                LV = self.getLinearVelocity(d, LV, 180-angle)
                AV = self.getAngularVelocity(d, 180-angle)
            elif angle >= -90 and angle < 0:
                LV = self.getLinearVelocity(d, LV, 0-angle)
                AV = self.getAngularVelocity(d, 0-angle)
            elif angle >= -180 and angle < -90:
                LV = self.getLinearVelocity(d, LV, 180+angle)
                AV = 0 - self.getAngularVelocity(d, 180+angle)
            self.twist.linear.x = LV
            self.twist.angular.z = AV
            print('ACTION!! LV:' + str(LV) + ', AV:' + str(AV))

        self.cmd_vel_pub.publish(self.twist)
        
    # Input:
    #   d: The distance from bot to obstacle
    #   LV: Current bot linear velocity
    #   angle: angle between this beam (obstacle) and X axis
    # Output:
    #   LV: New bot linear velocity
    def getLinearVelocity(self, d, LV, angle):
        LV = self.LV_MIN + (LV - self.LV_MIN) * d * math.sin(math.radians(angle)) / self.D_MAX
        print('\tLV=' + str(LV))
        return LV

    # Input:
    #   d: The distance from bot to obstacle
    #   angle: angle between this beam (obstacle) and X axis
    # Output:
    #   AV: New bot angular velocity
    def getAngularVelocity(self, d, angle):
        AV = self.AV_FACTOR * (self.AV_MIN + (self.AV_MAX - self.AV_MIN) * (1 - d * math.sin(math.radians(angle)) / self.D_MAX))
        print('\tAV=' + str(AV))
        return AV
        
if __name__ == '__main__':
    #print('start')
    rospy.init_node('main')
    run = main()
    rospy.spin()
    

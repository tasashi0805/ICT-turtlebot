#! /usr/bin/env python

import sys
import math
import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image, CameraInfo, CompressedImage, LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidanceRedLineFollowing:
    def __init__(self):
	    rospy.init_node('obstacle_avoidance', anonymous=True)   # initialize node
        #rospy.init_node('drive')     should not have 2 node


        self.D_MAX = 0.5     # MAX_OBSTACLE_DISTANCE detection

        self.LV_MIN = 0.1    # MIN_LINEAR_VELOCITY
        self.LV_MAX = 2.6     # MAX_LINEAR_VELOCITY

        self.AV_MIN = 0.3     # MAX_ANGULAR_VELOCITY
        self.AV_MAX = 1.82     # MAX_ANGULAR_VELOCITY
        self.AV_FACTOR = 0.5    # adjuest performance

        self.DEFAULT_LV = 0.3   # DEFAULT_LINEAR_VELOCITY
        self.DEFAULT_AV = 0.0    # DEFAULT_ANGULAR_VELOCITY

        self.cloest_obtacle_distance = 1000   #ininiate cloest_obtacle_distance
        
        self.sub = rospy.Subscriber('scan', LaserScan, self.laserScanCallback)  # define subscriber with name "scan"
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)   # define publisher with name "cmd_vel" # queue: cache of message
        
        self.move = Twist() # get velocity info
        self.run()
        
        
        print('init')
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw/compressed', CompressedImage, self.image_callback)
        self.cnt = 0
        
    def run(self):
        
        self.printDefaultValues()   # print default parameter values
        rospy.spin()

    def printDefaultValues(self):   # print default parameter values
        print('D_MAX = ' + str(self.D_MAX) + '\t# MAX_OBSTACLE_DISTANCE detection')
        print('LV_MAX = ' + str(self.LV_MAX) + '\t# MAX_LINEAR_VELOCITY')
        print('LV_MIN = ' + str(self.LV_MIN) + '\t# MIN_LINEAR_VELOCITY')
        print('AV_MAX = ' + str(self.AV_MAX) + '\t# MAX_ANGULAR_VELOCITY')
        print('AV_MIN = ' + str(self.AV_MIN) + '\t# MIN_ANGULAR_VELOCITY')
        print('DEFAULT_LV = ' + str(self.DEFAULT_LV) + '\t# DEFAULT_LINEAR_VELOCITY')
        print('DEFAULT_AV = ' + str(self.DEFAULT_AV) + '\t# DEFAULT_ANGULAR_VELOCITY')
        
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

    # Input:
    #   msg: Data returned from callback function
    # Output:
    #   AV: New bot angular velocity
    def laserScanCallback(self, msg):
        self.move.linear.x = self.DEFAULT_LV
        self.move.angular.z = self.DEFAULT_AV

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
            LV = self.DEFAULT_LV
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
            self.move.linear.x = LV
            self.move.angular.z = AV
            print('ACTION!! LV:' + str(LV) + ', AV:' + str(AV))

        self.pub.publish(self.move)
        
        
    def image_callback(self, msg):
        if self.cloest_obtacle_distance >= self.D_MAX:
            self.cnt += 1
            print(self.cnt)
            print('image')
            image = self.bridge.compressed_imgmsg_to_cv2(msg)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #detect color of the map that wanted  robot to follow

            red_lower_range = np.array([0,50,50])
            red_upper_range = np.array([10,255,255])
            mask = cv2.inRange(hsv, red_lower_range, red_upper_range)
    #shape of image 
            h, w, d = image.shape
            print("h:",h,"w",w,"d",d)
            search_top = 3*h/4
            print("search_top",search_top)
            search_bot = 3*h/4 + 20 
            print("search_bot",search_bot)
            mask[0:int(search_top), 0:w] = 0
            mask[int(search_bot):h, 0:w] = 0
    #get the center points of blob 
            M = cv2.moments(mask)
            if M['m00'] > 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
    #error numbers in the real environment when the robot moving 
                err = cx - w/2
                self.move.linear.x = 0.2
                self.move.angular.z = -float(err) /100
                self.pub.publish(self.move)
                print(err)

def main():
    try:
        odom = ObstacleAvoidanceRedLineFollowing()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
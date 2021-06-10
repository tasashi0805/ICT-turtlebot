#!/usr/bin/env python 


import rospy, cv2, cv_bridge
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import Image, CameraInfo, CompressedImage
from geometry_msgs.msg import Twist


class Drive:
	def __init__(self):
		print('init')
		self.bridge = cv_bridge.CvBridge()
		self.drive_pub = rospy.Publisher("drive",Float64,queue_size=10)
		self.image_sub = rospy.Subscriber('/camera/rgb/image_raw/compressed', CompressedImage, self.fn_image_from_cam)
		
		self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.twist = Twist()
		self.cnt = 0
		#when test in simulator
		self.alpha = 0.01
		#when test in real environment
		#self.alpha = 1/700
		self.speed = 0.2

	def fn_move_robot(self,error):
		#Speed to move
		self.twist.linear.x = self.speed
		#The angle of robot to move
		self.twist.angular.z = -float(error)*self.alpha
		#Publish to robot speed and angle
		self.velocity_publisher.publish(self.twist)

	def fn_image_from_cam(self, msg):
		#self.cnt += 1
		#print(self.cnt)
		#print('image')
		image = self.bridge.compressed_imgmsg_to_cv2(msg)
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#detect color of the map that wanted  robot to follow

		red_lower_range = np.array([0,50,50])
		red_upper_range = np.array([10,255,255])

		mask = cv2.inRange(hsv, red_lower_range, red_upper_range)
#displet the image
		#cv2.imshow("img:", mask)
		#cv2.waitKey(0)
		#shape of image 
		height, width, depth = image.shape
		
		top = 3*height/4
		bottom = 3*height/4 + 20 
		
		mask[0:int(top), 0:width] = 0
		mask[int(bottom):height, 0:width] = 0

#find then center of the blob using moments in OpenCV
#calculate the moment of the image 

		M = cv2.moments(mask)
#calculate x,y coordinate of center 
		if M['m00'] <= 0:
			return
		center_of_line_x = int(M['m10']/M['m00'])
		center_of_line_y = int(M['m01']/M['m00'])
#error value in the real environment when the robot moving 
		error = center_of_line_x - width/2
		self.fn_move_robot(error)
		print("The error of robot from the line",error)

if __name__ == '__main__':
	print('start')
	rospy.init_node('drive')
	drive = Drive()
	rospy.spin()

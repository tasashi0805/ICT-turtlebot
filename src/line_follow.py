#!/usr/bin/env python 


import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image, CameraInfo, CompressedImage
from geometry_msgs.msg import Twist


class Drive:
	def __init__(self):
		print('init')
		self.bridge = cv_bridge.CvBridge()
		self.drive.pud=rospy.Publisher("drive",Float64,queue_size=10)
		self.image_sub = rospy.Subscriber('/camera/rgb/image_raw/compressed', CompressedImage, self.image_callback)
		
		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.twist = Twist()
		self.cnt = 0

	def image_callback(self, msg):
		self.cnt += 1
		print(self.cnt)
		print('image')
		#image = self.bridge.imgsg_to_cv2(msg,desired_encoding='bgr8')
		image = self.bridge.compressed_imgmsg_to_cv2(msg)
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#detect color of the map that wanted  robot to follow

		red_lower_range = np.array([0,50,50])
		red_upper_range = np.array([10,255,255])
		mask = cv2.inRange(hsv, red_lower_range, red_upper_range)
		#cv2.imshow("img:", mask)
		#cv2.waitKey(0)
#shape of image 
		height, width, deep = image.shape
		
		search_top = 3*height/4
		
		search_bot = 3*height/4 + 20 
		
		mask[0:int(search_top), 0:width] = 0
		mask[int(search_bot):height, 0:width] = 0

#calculate the moment of the image 

		M = cv2.moments(mask)
		if M['m00'] > 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

#error value in the real environment when the robot moving 
			error = cx - width/2
			self.twist.linear.x = 0.2

			self.twist.angular.z = -float(error) /700
			#self.twist.angular.z = -float(error) /1000

			self.cmd_vel_pub.publish(self.twist)
			print("error:",error)

		##cv2.imshow("mask",mask)
		##cv2.imshow("output", image)
		##print("output Image")
		##cv2.waitKey(3)#display the window until any keypress 
		#cv2.waitkey(1) #display a frame for 1ms, after that 
if __name__ == '__main__':
	print('start')
	rospy.init_node('drive')
	drive = Drive()
	rospy.spin()

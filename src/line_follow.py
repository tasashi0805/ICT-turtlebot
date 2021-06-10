#!/usr/bin/env python 

import rospy, cv2, cv_bridge
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Twist


class Drive:
	def __init__(self):
		self.bridge = cv_bridge.CvBridge()
		self.drive_pub= rospy.Publisher("drive",Float64,queue_size=10)
		self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.twist = Twist()
		self.cnt = 0

	def image_callback(self, msg):
		self.cnt += 1
		image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#detect color of the map that wanted  robot to follow

		red_lower_range = np.array([0,50,50])
		red_upper_range = np.array([10,255,255])
		mask = cv2.inRange(hsv, red_lower_range, red_upper_range)
		#cv2.imshow("img:", mask)
		#cv2.waitKey(0)
#shape of image 
		height, width, deep = image.shape
		top = 3*height/4
		bottom = 3*height/4 + 20 

		mask[0:int(top), 0:width] = 0
		mask[int(bottom):height, 0:width] = 0

#find then center of the blob using moments in OpenCV
#get the center points of blob 
		M = cv2.moments(mask)
#calculate x,y coordinate of center
		if M['m00'] > 0:
			center_of_line_x = int(M['m10']/M['m00'])
			center_of_line_y = int(M['m01']/M['m00'])
#error numbers in the real environment when the robot moving 
			err = center_of_line_x - width/2

			#self.twist.angular.z = -float(err) /1000
			self.drive_pub.publish(err)

		
if __name__ == '__main__':
	print('start')
	rospy.init_node('drive')
	drive = Drive()
	rospy.spin()


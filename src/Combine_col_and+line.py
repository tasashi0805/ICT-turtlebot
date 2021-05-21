#!/usr/bin/env python 


import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image, CameraInfo, CompressedImage
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class Drive:
	def __init__(self):
		print('init')
		self.bridge = cv_bridge.CvBridge()
		#self.image_pub = rospy.Publisher('modified_image', CompressedImage, queue_size=10)
		#self.image_sub = rospy.Subscriber('/camera/rgb/image_raw/compressed', CompressedImage, self.image_callback)
		self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
		self.colorsub= rospy.Subscriber("color",String, self.col_msg_callback)

		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		#self.msg_pub= rospy.Publisher("drive", Float64, queue_size=1)

		self.twist = Twist()

	def image_callback(self, msg):
		#print(self.cnt)
		#print('image')
		image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
	#	image = self.bridge.compressed_imgmsg_to_cv2(msg)
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#detect color of the map that wanted  robot to follow

		red_lower_range = np.array([0,50,50])
		red_upper_range = np.array([10,255,255])
		mask = cv2.inRange(hsv, red_lower_range, red_upper_range)
		#cv2.imshow("img:", mask)
		#cv2.waitKey(0)
#shape of image 
		h, w, d = image.shape
		#print("h:",h,"w",w,"d",d)
		search_top = 3*h/4
		#print("search_top",search_top)
		search_bot = 3*h/4 + 20 
		#print("search_bot",search_bot)
		mask[0:int(search_top), 0:w] = 0
		mask[int(search_bot):h, 0:w] = 0
#get the center points of blob 
		M = cv2.moments(mask)
		if M['m00'] > 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
#error numbers in the real environment when the robot moving 
			err = cx - w/2
			#1000 for real turtlebot
			self.twist.angular.z = -float(err) /1000
			self.cmd_vel_pub.publish(self.twist)

		#print("err",err)
		##cv2.imshow("mask",mask)
		##cv2.imshow("output", image)
		##print("output Image")
		##cv2.waitKey(3)#display the window until any keypress 
		#cv2.waitkey(1) #display a frame for 1ms, after that 
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



if __name__ == '__main__':
	#print('start')
	rospy.init_node('drive')
	drive = Drive()
	rospy.spin()
	

#!/usr/bin/env python
import cv2
import numpy as np
import rospy
import sys
import time
from rospy.impl.tcpros_base import TCPROS

#import ROS msg 
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from nav_msgs.msg import Odometry


class colourdetect:
	def __init__(self):
		#print("==========color card class =================")

	# Set up  subscriber and pbulisher  define value
		self.sub=rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
		self.color_pub= rospy.Publisher("color",String,queue_size=10)
		self.pub=rospy.Publisher("/cmd_vel",Twist, queue_size=1)
		self.move= Twist()

		self.stop=0
	
	def colorsize(self,mask,cv2_img):
		check_mask=np.sum(mask)
		if check_mask>0:
			cnts =cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			cnts=sorted(cnts, key=cv2.contourArea)
			#print(len(cnts))
			#check all the cnts in the map
			if len(cnts) >=1 :
				for c in cnts:
					x,y,w,h=cv2.boundingRect(c)
					#crop the origin img for position y and x
					if w>300 and h>200:
						cv2.putText(cv2_img,"w={},h={}".format(w,h),(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(36,255,12),2)
						#cv2.imshow("mask:", cv2_img)
						#cv2.waitKey(3)
						return(w,h)
					else:
						return (0,0)
		else:
			return (0,0)


	def image_callback(self, msg):
		bridge = CvBridge()
		# Convert your ROS Image message to OpenCV2
		cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")

		#hsv
		hsv= cv2.cvtColor(cv2_img,cv2.COLOR_BGR2HSV)

		#blue color range and mask	
		blue_lower_range = np.array([110,50,50])
		blue_upper_range = np.array([130,255,255])
		blue_mask = cv2.inRange(hsv, blue_lower_range, blue_upper_range)
		
		#red color range and mask
		#red color range start with 0 to 10 and 160 to 189
		red_lower_range = np.array([0,50,50])
		red_upper_range = np.array([10,255,255])
		red_mask0= cv2.inRange(hsv, red_lower_range, red_upper_range)
		
		red_lower_range=np.array([169,50,50])
		red_upper_range=np.array([189, 255, 255])
		red_mask1 = cv2.inRange(hsv, red_lower_range, red_upper_range)
		red_mask= red_mask0+red_mask1


		#green color range and mask
		green_lower_range=np.array([50,100,50])
		green_upper_range=np.array([70, 255, 255])
		green_mask = cv2.inRange(hsv, green_lower_range, green_upper_range)
					
		# FInd contours in image
		
		#cv2.imshow("img:",cv2_img)
		#cv2.waitKey(0)
		
		# get bue red green object into color size function
		# if the color has 4 contor then it will return there w and h 
		
		bcw,bch=self.colorsize(blue_mask,cv2_img)
		rcw,rch=self.colorsize(red_mask,cv2_img)
		gcw,gch=self.colorsize(green_mask,cv2_img)
		#print("bcw:",bcw,"bch:",bch)
		#print("rcw:",rcw,"rch:",rch)
		#print("gcw:",gcw,"gch:",gch)
		
		# twist is a package for determine the robot speed and position(turn right or left)
		#testing for no line follow

		# condition color and pixel size 
		# if w and h has a high value than it will trigger some 
		if  bcw>0 and bch>0:
			print("blue color card trigger")
			#increase speed
			color="blue"
		#w=356 h==230
			#red card stop fimction
		elif rcw>640 and rch>400 and rcw<740 and rch<500:
			print("red color trigger")
			color="red"
			

		elif gcw>510 and gch>300:
			print("green color trigger")
			color="green"
		else:
			color="No"
		
		self.color_pub.publish(color)

def main():
	ic = colourdetect()
	rospy.init_node('detect_color_card', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
    main()

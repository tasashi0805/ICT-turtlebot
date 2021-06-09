#!/usr/bin/env python
import cv2
import numpy as np
import rospy

from rospy.impl.tcpros_base import TCPROS

#import ROS msg 
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError


class colourdetect:
	def __init__(self):
		# Set up  subscriber and publisher define value
		# Subscribe carmera 
		self.sub=rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
		self.color_pub= rospy.Publisher("color",String,queue_size=10)
		self.pub=rospy.Publisher("/cmd_vel",Twist, queue_size=1)
		self.move= Twist()
		self.CH=300 # for blue and green card min height  
		self.CW=400 # for blue and green card min weight
		
		# purpose of this part is stop when it detect red card
		# Also when the program detect the red line, it will stop
		# avoid the above situation, i have to make a specific size range to avoid it stop when the camera detects the   
		self.RCH_min=640 # red card minuim height  
		self.RCW_min=400 # red card min weight
		self.RCH_max=740 # red card max height
		self.RCW_max=500 # red caed max weight 
		self.stop=0
	# This function purpose is get the object weight and height
	def colorsize(self,mask,cv2_img):
		check_mask=np.sum(mask)
		if check_mask>0:
			# have three outcome with findContours and we need the second output
			cnts =cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			cnts=sorted(cnts, key=cv2.contourArea)
			#extrac the W,H
			for c in cnts:
				x,y,w,h=cv2.boundingRect(c)
					#crop the origin img for position y and x
					#if w>100 and h>100:
						#cv2.putText(cv2_img,"w={},h={}".format(w,h),(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(36,255,12),2)
						#cv2.imshow("mask:", cv2_img)
						#cv2.waitKey(3)
				return(w,h)
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
					
		#debug check color mask. Mask only has two color back and white. White mean the object that detected 		
		#cv2.imshow("img:",cv2_img)
		#cv2.waitKey(0)
		
		# get blue red green object into color size function
		bcw,bch=self.colorsize(blue_mask,cv2_img)
		rcw,rch=self.colorsize(red_mask,cv2_img)
		gcw,gch=self.colorsize(green_mask,cv2_img)
		#debug meesage check color card size
		print("bcw:",bcw,"bch:",bch)
		#print("rcw:",rcw,"rch:",rch)
		#print("gcw:",gcw,"gch:",gch)
		
		# twist is a package for determine the robot speed and position(turn right or left)

		# condition color and pixel size 
		# if w and h has a high value than it will trigger some event
		
		# Using publisher to publish the blue color message to main  
		if  (bcw>self.CW or bch>self.CH):
			print("blue color card trigger")
			#increase speed
			color="blue"	
			# return red message
		elif rcw>self.RCH_min and rch>self.RCW_min and rcw<self.RCH_max and rch<self.RCW_max:
			print("red color trigger")
			color="red"
			
			# return green message 
		elif gcw>self.CW and gch>self.CH:
			print("green color trigger")
			color="green"
		# return No color detect message
		else:
			color="No"
		# publish to color topic (color node)
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

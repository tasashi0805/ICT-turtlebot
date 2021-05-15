#!/usr/bin/env python
import cv2
import numpy as np
import rospy
import sys
import time

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from nav_msgs.msg import Odometry


class colourdetect:
	def __init__(self):
		print("==========color card class =================")
	# Set up your subscriber and define its callback
		self.sub=rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
		self.pub=rospy.Publisher("/cmd_vel",Twist, queue_size=10)
		self.move= Twist()
		self.speedup=0.4
		self.speedslow=0.15
		self.defaultspeed=0.2

		self.stop=0
	def colorsize(self,mask,cv2_img):
		check_mask=np.sum(mask)
		if check_mask>0:
			cnts =cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			cnts=sorted(cnts, key=cv2.contourArea)
			#print(len(cnts))
			if len(cnts) >=1 :
				cntrRect=[]
				for c in cnts:
					x,y,w,h=cv2.boundingRect(c)
					#crop the origin img for position y and x
					new_contour= cv2_img[y:y+h, x:x+w]
					epsilon = 0.05*cv2.arcLength(c,True)
					approx = cv2.approxPolyDP(c,epsilon,True)
					if len(approx) == 4:
						cv2.rectangle(cv2_img,(x,y),(x+w,y+h),(36,255,12),2)
						#cv2.putText(cv2_img,"w={},h={}".format(w,h),(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(36,255,12),2)
						#cv2.imshow("mask:", cv2_img)


						return(w,h)
					else:
						return (0,0)
		else:
			return (0,0)


	def image_callback(self, msg):
		print("--------image_callback-------------")
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
		red_lower_range = np.array([0,50,50])
		red_upper_range = np.array([10,255,255])
		red_mask0= cv2.inRange(hsv, red_lower_range, red_upper_range)
		
		red_lower_range=np.array([169,50,50])
		red_upper_range=np.array([189, 255, 255])
		red_mask1 = cv2.inRange(hsv, red_lower_range, red_upper_range)
		
		red_mask= red_mask0+red_mask1

		#cv2.imshow("red:",red_mask)
		#cv2.waitKey(0)
		#green color range and mask
		green_lower_range=np.array([50,100,50])
		green_upper_range=np.array([70, 255, 255])
		green_mask = cv2.inRange(hsv, green_lower_range, green_upper_range)
					
		# FInd contours in image
		
		#cv2.imshow("img:",cv2_img)
		#cv2.waitKey(0)
		
		bcw,bch=self.colorsize(blue_mask,cv2_img)
		
		if bcw and bch !=0:
			print("bcw:",bcw,"bch:",bch)
		rcw,rch=self.colorsize(red_mask,cv2_img)
		print("rcw:",rcw,"rch:",rch)
		gcw,gch=self.colorsize(green_mask,cv2_img)
		
		hasblue=np.sum(blue_mask)
		hasred=np.sum(red_mask)
		hasgreen=np.sum(green_mask)

		# twist is a package for determine the robot speed and position(turn right or left)
		#testing
		self.move.linear.x=self.defaultspeed
		self.pub.publish(self.move)

		print("currentspeed:",self.move.linear.x)
		# condition color and pixel size
		if hasblue>0 and bcw>300 and bch>200 and self.move.linear.x< self.speedup:
			print("blue color card trigger")
			#increase speed
			self.move.linear.x=self.speedup
			self.pub.publish(self.move)
			# 3 second with increase speed funciton
			time.sleep(3)	
			# return to default speed
			self.move.linear.x=self.defaultspeed
			self.pub.publish(self.move)

			
				#red card stop fimction
		elif hasred>0 and rcw>300 and rch>200 and rcw<800 and rch<500:
			print("red color trigger")

			
			self.move.linear.x=self.stop
			self.pub.publish(self.move)
			

		elif hasgreen>0 and gcw>300 and gch>200 and gcw<400 and gch<300:
			print("green color trigger")
					# Decrease speed for 3 sec
			self.move.linear.x=self.speedslow
			self.pub.publish(self.move)
			#publish msg	
								

			time.sleep(3)
					
			# default speed
			self.move.linear.x=self.defaultspeed
					#print("green:",twist_msg.linear)
			self.pub.publish(self.move)	
			detectgreencolor=False	
				#print(twist_msg)

def main(args):
	ic = colourdetect()
	rospy.init_node('detect_color_card', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

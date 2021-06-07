#!/usr/bin/env python
import cv2
import numpy as np
import rospy
import sys
import time

#import ROS msg 
from sensor_msgs.msg import Image, CompressedImage
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError



class colourdetect:
	def __init__(self):
		print("==========color card class =================")
	# Set up your subscriber and define its callback
		#Realworld subsribe node
		self.sub=rospy.Subscriber("/raspicam_node/image/compressed", CompressedImage, self.image_callback)
		
		#Simulator
		#self.sub=rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, self.image_callback)

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
			print("cnts:",len(cnts))
			#print(len(cnts))
			#check all the cnts in the map
			for c in cnts:
				x,y,w,h=cv2.boundingRect(c)
				print(x,y,w,h)
				#crop the origin img for position y and x	
				if w>70 and h>50:
					cv2.putText(cv2_img,"w={},h={}".format(w,h),(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(36,255,12),2)
					#cv2.imshow("mask:", cv2_img)
					#cv2.waitKey(3)
					return(w,h)
				else:
					return (0,0)
		else:
			return(0,0)



	def image_callback(self, msg):
		#print("--------color trigger -------------")
		bridge = CvBridge()
		# Convert your ROS Image message to OpenCV2
		cv2_img = bridge.compressed_imgmsg_to_cv2(msg)

		#hsv
		hsv= cv2.cvtColor(cv2_img,cv2.COLOR_BGR2HSV)



		#blue color range and mask	
		blue_lower_range = np.array([100,50,0])
		blue_upper_range = np.array([120,255,200])
		blue_mask = cv2.inRange(hsv, blue_lower_range, blue_upper_range)
		#cv2.imshow("mask:", blue_mask)
		#cv2.waitKey(3)
		#red color range and mask
		#red color range start with 0 to 10 and 160 to 189
		#red_lower_range = np.array([0,50,50])
		#red_upper_range = np.array([10,255,255])
		#red_mask0= cv2.inRange(hsv, red_lower_range, red_upper_range)

		red_lower_range=np.array([169,50,50])
		red_upper_range=np.array([189, 255, 255])
		red_mask1 = cv2.inRange(hsv, red_lower_range, red_upper_range)		
		red_mask= red_mask1


		#cv2.imshow("red:",red_mask)
		#cv2.waitKey(0)
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
		print("bcw:",bcw,"bch:",bch)
		print("rcw:",rcw,"rch:",rch)
		print("gcw:",gcw,"gch:",gch)
		cv2.imshow("mask:", red_mask)
		cv2.waitKey(3)


		# twist is a package for determine the robot speed and position(turn right or left)
		#testing for no line follow


		# condition color and pixel size 
		# if w and h has a high value than it will trigger some 
		if bcw>0 and bcw<110 and bch<0 and bch<60:
			print("blue color card trigger")
			#increase speed
			#self.move.linear.x=self.speedup
			#self.pub.publish(self.move)
			#print("currentspeed:",self.move.linear.x)
			# 3 second with increase speed funciton
			#time.sleep(3)	
			# return to default speed
			#self.move.linear.x=self.defaultspeed
			#self.pub.publish(self.move)

			
				#red card stop fimction
		elif rcw>300 and rch>200 :
			print("red color trigger")
			#self.move.linear.x=self.stop
			#self.pub.publish(self.move)
			#print("currentspeed:",self.move.linear.x)
			

		elif gcw>0 and gch>0:
			print("green color trigger")
			# Decrease speed for 3 sec
			#self.move.linear.x=self.speedslow
			#publish msg						
			#self.pub.publish(self.move)
			#print("currentspeed:",self.move.linear.x)
			#time.sleep(3)
			# return default speed
			#self.move.linear.x=self.defaultspeed
			#print("green:",twist_msg.linear)
			#self.pub.publish(self.move)	

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

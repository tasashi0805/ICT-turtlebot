#!/usr/bin/env python 



import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64,Float32MultiArray

import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64


class mainClass:
	def __init__(self):
		print('init')
		self.colorsub= rospy.Subscriber("color",String, self.col_msg_callback)
		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.drive_sub= rospy.Subscriber("drive",Float64, self.linefollowcallback)

		self.obsscb=rospy.Subscriber("obstacle_to_main",Float32MultiArray,self.obscallback)
		#self.msg_pub= rospy.Publisher("drive", Float64, queue_size=1)
		self.twist = Twist()
		self.state1=False

		#self.obsscb=rospy.Subscriber("obstacle_to_main",Float64,self.obscallback)
		#self.msg_pub= rospy.Publisher("drive", Float64, queue_size=1)
		self.twist = Twist()

	def col_msg_callback(self,msg):
		data=msg.data
		if data=="blue":
			self.twist.linear.x=0.4
		elif data=="green":
			self.twist.linear.x=0.1
		elif data=="red":
			self.twist.linear.x=0
			self.cmd_vel_pub.publish(self.twist)
		else:
			data="No"
			if self.state1==False:
			#if (self.twist.linear.x>0 and self.twist.linear.x<0.2):
				self.twist.linear.x=0.2
				#self.cmd_vel_pub.publish(self.twist)
		
		print("Speed:",self.twist.linear.x)

			print("Speed:",self.twist.linear)
			self.cmd_vel_pub.publish(self.twist)
		else:
			data="No"
			self.twist.linear.x=0.2
			self.cmd_vel_pub.publish(self.twist)

		
		print("Speed:",self.twist.linear)
		returnvalue=self.twist.linear.x

		self.cmd_vel_pub.publish(self.twist)
	
	def linefollowcallback(self,msg):
		data=msg.data
		err = -float(data) /1000
		self.twist.angular.z=err

		self.cmd_vel_pub.publish(self.twist)

	def obscallback(self,msg):
		self.state1=True
		linearx=msg.data[0]
		angularz=msg.data[1]
		#linearx, angularz=msg.data
		self.twist.linear.x=linearx
		self.twist.angular.z=angularz
		if self.state1==True:
			self.twist.linear.x=0.2
			self.state1=False
		self.cmd_vel_pub.publish(self.twist)

		returnvalue=self.twist.angular.z
		self.cmd_vel_pub.publish(self.twist)

		




def main():
	rospy.init_node('main')
	run = mainClass()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
    main()

	

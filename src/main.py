#!/usr/bin/env python 


import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64

class main:
	def __init__(self):
		print('init')
		self.colorsub= rospy.Subscriber("color",String, self.col_msg_callback)
		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
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
			print("Speed:",self.twist.linear)
			self.cmd_vel_pub.publish(self.twist)

		elif data=="No":
			self.twist.linear.x=0.2
		print("Speed:",self.twist.linear)
		self.cmd_vel_pub.publish(self.twist)



if __name__ == '__main__':
	#print('start')
	rospy.init_node('main')
	run = main()
	rospy.spin()
	

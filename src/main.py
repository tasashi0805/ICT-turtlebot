#!/usr/bin/env python 
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64,Float32MultiArray

from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64

# default speed 0.2
class mainClass:
	def __init__(self):
		# recevice message from three class 
		# publish message to Twist (determine the robot movement)		
		self.colorsub= rospy.Subscriber("color",String, self.col_msg_callback)
		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.drive_sub= rospy.Subscriber("drive",Float64, self.linefollowcallback)

		self.obsscb=rospy.Subscriber("obstacle_to_main",Float32MultiArray,self.obscallback)
		self.twist = Twist()
		self.state1=False
		self.defaultspeed=0.2
		self.speedup=self.defaultspeed*2
		self.stop=0
		self.speedslow=0.1
		self.twist = Twist()
	#get message from the color publisher  and adust speed for different color
	def col_msg_callback(self,msg):
		#msg datatype float
		data=msg.data
		if data=="blue":
			self.twist.linear.x=self.speedup
		elif data=="green":
			self.twist.linear.x=self.speedslow
		elif data=="red":
			self.twist.linear.x=self.stop
			self.cmd_vel_pub.publish(self.twist)
		else:
			data="No"
			if self.state1==False:
			#if (self.twist.linear.x>0 and self.twist.linear.x<0.2):
				self.twist.linear.x=self.defaultspeed
				#self.cmd_vel_pub.publish(self.twist)		
		print("Speed:",self.twist.linear)

		self.cmd_vel_pub.publish(self.twist)
	#get message from the linefollow publisher and adjust the angular
	def linefollowcallback(self,msg):
		#msg datatype float
		data=msg.data
		err = -float(data) /1000
		self.twist.angular.z=err

		self.cmd_vel_pub.publish(self.twist)
	#get message from the obstacle avoidance publisher and adjust the linear and angular when there is an obstacle on the path
	def obscallback(self,msg):
		# msg datatype is float array
		self.state1=True
		linearx=msg.data[0]
		angularz=msg.data[1]
		self.twist.linear.x=linearx
		self.twist.angular.z=angularz
		if self.state1==True:
			self.twist.linear.x=self.defaultspeed
			self.state1=False
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

	

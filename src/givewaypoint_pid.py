#!/usr/bin/env python
import rospy
import PID
import numpy as np
import matplotlib.pyplot as plt
import time
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseStamped
from mav_msgs.msg import Actuators
import time

def publish_waypoint(x,y,z,yaw):
	"""
	Publish a waypoint to 
	"""
	print("here")

	plotz = []
	plot1 = []
	t = []
	
    	start_time = time.time()

	pub = rospy.Publisher('/hummingbird/command/motor_speed', Actuators, queue_size = 1)
	acc = Actuators()

	pid = PID.PID(130, 0, 100)

	while True:
		#read position
		data = None
		data = rospy.wait_for_message('/hummingbird/odometry_sensor1/position', PointStamped, timeout=1)
		    
		plotz.append(data.point.z)
		plot1.append(z)
		
		plt.plot(plotz, color='blue')
		plt.plot(plot1, color='red')
		plt.pause(0.000001)

		error = z - data.point.z
		throttle = pid.Update(error)
		print(error)
		t.append(throttle)

		acc.angular_velocities = [throttle, throttle, throttle, throttle]
		pub.publish(acc)

		if(data.point.z > 20):
			acc.angular_velocities = [0, 0, 0, 0]
			pub.publish(acc)
			break
			

		if(error * 130 > 500):
			print("abbbbbbbbbb huaaa") 


if __name__ == '__main__':
	
	rospy.init_node("rotors_waypoint_publisher", anonymous = True)

	# get command line params
	x_des = 0
	y_des = 0
	z_des = 10.0
	yaw_des = 0

	publish_waypoint(x_des, y_des, z_des, yaw_des)

	

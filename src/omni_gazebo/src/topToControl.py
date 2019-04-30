#base on 1.13version.py
# witre in jur 19th 5:26pm try to cut two part one subscriber from '/cmd_vel' to control
# the robot another to lisren from robot's odom

import rospy
import socket
import time
import struct
from geometry_msgs.msg import Twist, Quaternion
from nav_msgs.msg import Odometry
import tf
from math import radians, copysign
from math import pi
import math
import Queue
import threading

class baseCon():

	def __init__(self):
	    #set node
		rospy.init_node('baseController', anonymous=False)

		#socket communication
	    	# self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	    	# self.sock.connect(('192.168.1.32', 5555))
		#self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=50)

		

		#self.rate = 25 #rospy.get_param('~rate',25)  # the rate at which to publish the transform
	    	self.L = 0.24905 #base_width = 0.4804 #float(rospy.get_param('~base_width', 0.4)) # in meters
		self.radius = 0.06325

		self.flag_frame_id = rospy.get_param('~flag_frame_id','flag')

		self.rate = rospy.Rate(25) # 25hz

		self.x = 0.0
		self.y = 0.0
		self.th = 0.0

		self.vx = 0
		self.vy = 0
		self.vth = 0

		while 1:
			rospy.Subscriber('/cmd_vel', Twist, self.callback)


	#definition call back
	def callback(self, move_cmd):
	    	len = 11
	    	MaxSpeed=0.55 #m/s
	    	MinSpeed=-0.55  #m/s


		#stop
		s = [0x5a,0x66,0x07,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x01]
		#forward
		f = [0x5a,0x66,0x07,0x01,0xfe,0x0c,0x01,0xf4,0x00,0x00,0x06]

		#turn left
		tl = [0x5a,0x66,0x07,0x01,0x01,0xf4,0x01,0xf4,0x01,0xf4,0xf4]
		tr = [0x5a,0x66,0x07,0x01,0xfe,0x0c,0xfe,0x0c,0xfe,0x0c,0xf3]


		#back
		b = [0x5a,0x66,0x07,0x01,0x01,0xf4,0xfe,0x0c,0x00,0x00,0x06]

		#anyspeed
		asp = [0x5a,0x66,0x07,0x01,0x01,0xf4,0xfe,0x0c,0x00,0x00,0x06]



	    	L = self.L #
	    	r = self.radius #    0.06325
	    	angle = math.pi / 6
	    	sina = 0.5 #math.sin(angle)
	    	cosa = math.cos(angle)

	    	vx = move_cmd.linear.x

	    	vy = move_cmd.linear.y

	    	w=move_cmd.angular.z
	    	#angular velocity of three wheel (rad/s)
	    	wtheta1 = (sina * vy - cosa * vx + w * L) / r    #-0.17 when pub x=0.2,y=0,z=0
	    	wtheta2 = (sina * vy + cosa * vx + w * L) / r    #-0.17 when pub x=0.2,y=0,z=0
	    	wtheta3 = (-vy + w * L) / r

	    	rads18000 = 83 * 2 * math.pi / 60 #8.691739674931762 rad/s

	    	k1 = int(wtheta1 * 18000 / rads18000) #set rad number to wheelA
	    	k2 = int(wtheta2 * 18000 / rads18000)
	    	k3 = int(wtheta3 * 18000 / rads18000)

	    	if k1 > 18000:
			k1 = 18000
	    	if k1 < -18000:
			k1 = -18000
	    	if k2 > 18000:
			k2 = 18000
	    	if k2 < -18000:
			k2 = -18000
	    	if k3 > 18000:
			k3 = 18000
	    	if k3 < -18000:
			k3 = -18000


	    	asp[4]=(k1>>8)&0xFF#vlint1
		asp[5]=k1 & 0xFF

		asp[6]=(k2>>8)&0xFF  #vrint1
		asp[7]=k2 & 0xFF

	    	asp[8]=(k3>>8)&0xFF#vlint2
	    	asp[9]=k3 & 0xFF

	    	asp[10]=asp[3]^asp[4]^asp[5]^asp[6]^asp[7]^asp[8]^asp[9]


	    	print repr(asp)
	    	for i in range(0,11):
			print('%x'%asp[i])
	    	data = struct.pack("%dB"%(len),*asp)
	    	self.sock.send(data)

if __name__ == '__main__':
    	baseCon()

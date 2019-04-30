#!/usr/bin/env python
# -- coding: utf-8 --

#导入库
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

class BaseController():

	def __init__(self):
	    #初始化节点
	    rospy.init_node('baseController', anonymous=False)
	    #socket通信
	    # self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	    # self.sock.connect(('192.168.1.32', 5555))
		# self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=50)
		##parameter
		self.rate = 25 #rospy.get_param('~rate',25)  # the rate at which to publish the transform
	    self.L = 0.24905 #base_width = 0.4804 #float(rospy.get_param('~base_width', 0.4)) # in meters
		self.radius = 0.06325
		self.base_frame_id = rospy.get_param('~base_frame_id','base_link') # the name of the base frame of the robot
		self.odom_frame_id = rospy.get_param('~odom_frame_id', 'odom') # the name of the odometry reference frame

		self.rate = rospy.Rate(25) # 25hz
		self.odom_broadcaster = tf.TransformBroadcaster()
		self.enq=Queue.Queue() #缓冲编码器读数


		self.x = 0.0
		self.y = 0.0
		self.th = 0.0

		self.vx = 0
		self.vy = 0
		self.vth = 0

		self.current_time = rospy.get_time()
		self.last_time = rospy.get_time()
		self.last_Encoder1 = 0 #编码器1（A）的self.last_time时刻读数
		self.last_Encoder2 = 0 #编码器2（B）的self.last_time时刻读数
		self.last_Encoder3 = 0 #编码器3（C）的self.last_time时刻读数




		print rospy.get_time()

		thread2 = threading.Thread(target = self.thread02)
		thread2.setDaemon(True)
		thread2.start()
		thread1 = threading.Thread(target = self.thread01)
		thread1.setDaemon(True)
		thread1.start()

		rospy.spin()




	#定义第一个线程
	def thread01(self):
	    #订阅/cmd_vel话题
	    rospy.Subscriber('/cmd_vel', Twist, self.callback)


	#定义第一个线程
	def thread02(self):
	    #从串口接收编码器信息并发布
	    #while not rospy.is_shutdown():
	    r = rospy.Rate(25)
	    while  1:
		#self.talker3()
	self.talker()
	r.sleep()

	#定义回调函数
	def callback(self, move_cmd):
	    len = 11
	    MaxSpeed=0.55 #m/s
	    MinSpeed=-0.55  #m/s


	    #停止
		s = [0x5a,0x66,0x07,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x01]
		#前进
		f = [0x5a,0x66,0x07,0x01,0xfe,0x0c,0x01,0xf4,0x00,0x00,0x06]

		#左转
		tl = [0x5a,0x66,0x07,0x01,0x01,0xf4,0x01,0xf4,0x01,0xf4,0xf4]
		tr = [0x5a,0x66,0x07,0x01,0xfe,0x0c,0xfe,0x0c,0xfe,0x0c,0xf3]


		#后退
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
	    #三个轮子的角速度 rad/s
	    wtheta1 = (sina * vy - cosa * vx + w * L) / r    #-0.17 when pub x=0.2,y=0,z=0
	    wtheta2 = (sina * vy + cosa * vx + w * L) / r    #-0.17 when pub x=0.2,y=0,z=0
	    wtheta3 = (-vy + w * L) / r

	    rads18000 = 83 * 2 * math.pi / 60 #8.691739674931762 rad/s  设置为18000对应的轮子角速度

	    k1 = int(wtheta1 * 18000 / rads18000) #速度wtheta1对应的设置值
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


	def talker(self):
		#hello_str = "hello world %s" % rospy.get_time()
		#rospy.loginfo(hello_str)
		#pub.publish(hello_str)
		#print self.sock.recv(1024)

		len1=17

		buf = self.sock.recv(1024)
		if buf:
		    #data17 = repr(buf)
		    #for i in range(0,11):
		    #print ('%x'%repr(buf))
		    print("==========================start=================================")
		    self.current_time = rospy.get_time() #记录获得数据的当前时刻
		    timer = rospy.get_time()
		    print(self.current_time)
		    dt = self.current_time - self.last_time
		    self.last_time = self.current_time
		    #合法性判断todo （1）长度为17个字节，（2） data[16] 为data[3]~data[15]的异或
		    #合法则进行下面的工作

		    h0,h1,len2,uid,Encoder1,Encoder2,Encoder3,checksum=struct.unpack("!4c3ic",buf)
		    #记录编码器数据的增减

		    Encoder1_diff = Encoder1 - self.last_Encoder1
		    self.last_Encoder1 = Encoder1
		    Encoder2_diff = Encoder2 - self.last_Encoder2
		    self.last_Encoder1 = Encoder1
		    Encoder3_diff = Encoder3 - self.last_Encoder3
		    self.last_Encoder3 = Encoder3

		    #根据编码器读数转换为角速度 wtheta1，wtheta2，wtheta3
		    Ticks = 1224 #厂家提供实测一圈（2×math.pi弧度）对应的编码器点数
		    wrad1 = math.pi * 2 * Encoder1_diff / Ticks #Encoder1_diff点数对应的弧度数
		    wrad2 = math.pi * 2 * Encoder2_diff / Ticks #Encoder1_diff点数对应的弧度数
		    wrad3 = math.pi * 2 * Encoder3_diff / Ticks #Encoder1_diff点数对应的弧度数
		    wtheta1 = wrad1 / dt #角速度,rad/s
		    wtheta2 = wrad2 / dt #角速度,rad/s
		    wtheta3 = wrad3 / dt #角速度,rad/s

		    #转化为vx,vy,vth
		    angle = math.pi / 6
		    sina = 0.5 #math.sin(angle)
		    cosa = math.cos(angle)
		    tt = (wtheta1 + wtheta2 - 2 * wtheta3) / (2 + 2 * sina)
		    self.vx = self.radius * (wtheta2 - wtheta1) / ( 2 * cosa)
		    self.vy = self.radius * tt
		    self.vth = (wtheta3 + tt) * self.radius / self.L
		    if (self.vx != 0) or (self.vy != 0):
			delta_x = self.vx * dt
			delta_y = self.vy * dt
			# calculate the final position of the robot
		    self.x = self.x + ( math.cos( self.th ) * delta_x - math.sin( self.th ) * delta_y )
		    self.y = self.y + ( math.sin( self.th ) * delta_x + math.cos( self.th ) * delta_y )
		    if (self.vth != 0):
			delta_th = self.vth * dt
			self.th = self.th + delta_th

		    # publish the odom information
		    quaternion = Quaternion()
		    quaternion.x = 0.0
		    quaternion.y = 0.0
		    quaternion.z = math.sin( self.th / 2 )
		    quaternion.w = math.cos( self.th / 2 )
		    self.odom_broadcaster.sendTransform(
				(self.x, self.y, 0),
				(quaternion.x, quaternion.y, quaternion.z, quaternion.w),
				rospy.Time.now(),
				self.base_frame_id,
				self.odom_frame_id
				)
		    now=rospy.Time(0)
		    odom = Odometry()
		    odom.header.stamp = now
		    odom.header.frame_id = self.odom_frame_id
		    odom.pose.pose.position.x = self.x
		    odom.pose.pose.position.y = self.y
		    odom.pose.pose.position.z = 0
		    odom.pose.pose.orientation = quaternion
		    odom.child_frame_id = self.base_frame_id
		    odom.twist.twist.linear.x = self.vx
		    odom.twist.twist.linear.y = self.vy
		    odom.twist.twist.angular.z = self.vth
		    self.odom_pub.publish(odom)
		    print(dt)
		    #self.odom_broadcaster.sendTransform((self.x, self.y, 0),
		    #     tf.transformations.quaternion_from_euler(0, 0, self.th),
		    #     rospy.Time.now(),
		    #     "base_link",
		    #     "odom")

		    self.rate.sleep()


		#hello_str = "hello world %s" % rospy.get_time()
		#rospy.loginfo(hello_str)
		#pub.publish(hello_str)





if __name__ == '__main__':
    BaseController()

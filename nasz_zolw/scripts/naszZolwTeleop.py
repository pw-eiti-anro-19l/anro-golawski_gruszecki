#!/usr/bin/env python
import sys
import termios
import tty
import rospy

from geometry_msgs.msg import Twist

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
 		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def steering():
	pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
	rospy.init_node('naszZolwTeleop', anonymous=True)
	forward = rospy.get_param("naszZolwTeleop/forward")
	backward = rospy.get_param("naszZolwTeleop/backward")
	turn_left = rospy.get_param("naszZolwTeleop/turn_left")
	turn_right = rospy.get_param("naszZolwTeleop/turn_right")

	while True:
		key = getch()
		cmd = Twist()
		if key == forward:
			cmd.linear.x = 1.0
		elif key == backward:
			cmd.linear.x = -1.0
		elif key == turn_left:
			cmd.angular.z = 1.0
		elif key == turn_right:
			cmd.angular.z = -1.0

		pub.publish(cmd)
if __name__ == '__main__':
	try:
		steering()
	except rospy.ROSInterruptException:
		pass

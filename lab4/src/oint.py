#!/usr/bin/env python

import rospy
from lab4.srv import params2
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from std_msgs.msg import Header
import math

freq = 50
prev_pos = (1.0, -1., 1.)
prev_q = (0., 0., 0., 1.)
path = Path()


def handle_interpolation(data):
    if data.time <= 0.:
        return False
    global prev_pos
    global prev_q
    new_pos = (data.x, data.y, data.z)
    new_q = (data.qx, data.qy, data.qz, data.qw)
    rate = rospy.Rate(freq)

    current_time = 0.
    frames_number = int(math.ceil(data.time * freq))

    for i in range(frames_number+1):
        x = interpolate(prev_pos[0], new_pos[0], data.time, current_time, data.i)
        y = interpolate(prev_pos[1], new_pos[1], data.time, current_time, data.i)
        z = interpolate(prev_pos[2], new_pos[2], data.time, current_time, data.i)
        qx = interpolate(prev_q[0], new_q[0], data.time, current_time, data.i)
        qy = interpolate(prev_q[1], new_q[1], data.time, current_time, data.i)
        qz = interpolate(prev_q[2], new_q[2], data.time, current_time, data.i)
        qw = interpolate(prev_q[3], new_q[3], data.time, current_time, data.i)

        pose = PoseStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = 'base_link'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.x = qx
        pose.pose.orientation.y = qy
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw
        pub.publish(pose)

        path.header = pose.header
        path.poses.append(pose)
        path_pub.publish(path)
        current_time = current_time + 1.0 / freq
        rate.sleep()

    prev_pos = new_pos
    prev_q = new_q
    return True

def interpolate(start_j, last_j, time, current_time, i):
    if i == 1:
        return tri_int(start_j, last_j, time, current_time)
    else:
        return lin_int(start_j, last_j, time, current_time)

def lin_int(start_j, last_j, time, current_time):
    return start_j + (float(last_j - start_j) / time) * current_time

def tri_int(start_j, last_j, time, current_time):
    h = 2. * float(last_j - start_j) / time
    ratio = h / (time / 2.)
    if current_time < time / 2.:
        return start_j + current_time**2 * ratio / 2.
    else:
        return last_j - (time-current_time)**2 * ratio / 2.

if __name__ == "__main__":
    rospy.init_node('oint')
    pub = rospy.Publisher('oint_int', PoseStamped, queue_size=10)
    path_pub = rospy.Publisher('trace', Path, queue_size=10)
    s = rospy.Service('oint', params2, handle_interpolation)
    rospy.spin()

#!/usr/bin/env python

import rospy
from lab4.srv import params
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from std_msgs.msg import Header
import math

freq = 50
current_pos = [0.0, 0.0, 0.0]
path = Path()


def handle_interpolation(data):
    if data.time <= 0 or not -1 <= data.j1 <= 0 or not -1 <= data.j2 <= 0 or not -1 <= data.j3 <= 0:
        return False

    #current_pos = rospy.wait_for_message('joint_states', JointState, timeout = 10).position
    new_pos = [data.j1, data.j2, data.j3]
    diff_sum = sum([(new_pos[i] - current_pos[i]) for i in range(0, 3)])
    rate = rospy.Rate(freq)
    j1, j2, j3 = current_pos[0], current_pos[1], current_pos[2]

    frames_number = int(math.ceil(data.time * freq))
    current_time = 0.

    for k in range(0, frames_number + 1):
        computed_joint_state = JointState()
        computed_joint_state.header = Header()
        computed_joint_state.header.stamp = rospy.Time.now()
        computed_joint_state.name = ['base_to_link1', 'link1_to_link2', 'link2_to_link3']
        j1 = interpolate(current_pos[0], new_pos[0], data.time, current_time, data.i)
        j2 = interpolate(current_pos[1], new_pos[1], data.time, current_time, data.i)
        j3 = interpolate(current_pos[2], new_pos[2], data.time, current_time, data.i)
        computed_joint_state.position = [j1, j2, j3]
        computed_joint_state.velocity = []
        computed_joint_state.effort = []
        pub.publish(computed_joint_state)

        pose = PoseStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = 'hand'
        pose.pose.position.x = 0
        pose.pose.position.y = 0
        pose.pose.position.z = 0
        
        path.poses.append(pose)
        path_pub.publish(path)

        current_time = current_time + 1. / freq
        rate.sleep()
    current_position = [j1, j2, j3]
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
    rospy.init_node('jint')
    path.header.stamp = rospy.Time.now()
    path.header.frame_id = 'base_link'
    pub = rospy.Publisher('joint_states',JointState,queue_size=10)
    path_pub = rospy.Publisher('trace', Path, queue_size=10)
    s = rospy.Service('jint', params, handle_interpolation)
    rospy.spin()

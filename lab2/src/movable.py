#! /usr/bin/python

import rospy
import os
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker


def kinematics(data):
    x, y, z = (1, 0, 0), (0, 1, 0), (0, 0, 1)

    params = lines[0].split(" ")
    a, d, alfa, theta = params[0], params[1], params[2], params[3]
    a, d, alfa, theta = float(a), float(d), float(alfa), float(theta)  # conversion
    trans_z = translation_matrix((0, 0, d))
    rotate_z = rotation_matrix(theta, z)
    trans_x = translation_matrix((0, 0, a))
    rotate_x = rotation_matrix(alfa, x)
    T1 = concatenate_matrices(trans_z, rotate_z, trans_x, rotate_x)

    params = lines[1].split(" ")
    a, d, alfa, theta = params[0], params[1], params[2], params[3]
    a, d, alfa, theta = float(a), float(d), float(alfa), float(theta)  # conversion
    trans_z = translation_matrix((0, 0, d))
    rotate_z = rotation_matrix(theta, z)
    trans_x = translation_matrix((0, 0, a))
    rotate_x = rotation_matrix(alfa, x)
    T2 = concatenate_matrices(trans_z, rotate_z, trans_x, rotate_x)

    params = lines[2].split(" ")
    a, d, alfa, theta = params[0], params[1], params[2], params[3]
    a, d, alfa, theta = float(a), float(d), float(alfa), float(theta)  # conversion
    trans_z = translation_matrix((0, 0, d))
    rotate_z = rotation_matrix(theta, z)
    trans_x = translation_matrix((0, 0, a))
    rotate_x = rotation_matrix(alfa, x)
    T3 = concatenate_matrices(trans_z, rotate_z, trans_x, rotate_x)

    params = lines[3].split(" ")
    a, d, alfa, theta = params[0], params[1], params[2], params[3]
    a, d, alfa, theta = float(a), float(d), float(alfa), float(theta)  # conversion
    trans_z = translation_matrix((0, 0, d))
    rotate_z = rotation_matrix(theta, z)
    trans_x = translation_matrix((0, 0, a))
    rotate_x = rotation_matrix(alfa, x)
    T4 = concatenate_matrices(trans_z, rotate_z, trans_x, rotate_x)

    Tk = concatenate_matrices(T1, T2, T3, T4)
    x, y, z = translation_from_matrix(Tk)
    qx, qy, qz, qw = quaternion_from_matrix(Tk)

    pose = PoseStamped()
    pose.header.frame_id = 'base_link'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose.pose.orientation.x = qx
    pose.pose.orientation.y = qy
    pose.pose.orientation.z = qz
    pose.pose.orientation.w = qw
    pub.publish(pose)

    marker = Marker()
    marker.header.frame_id = 'base_link'
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.pose.orientation.w = 1

    time = rospy.Duration()
    marker.lifetime = time
    marker.scale.x = 0.07
    marker.scale.y = 0.07
    marker.scale.z = 0.07
    marker.pose.position.x = x;
    marker.pose.position.y = y;
    marker.pose.position.z = z;
    marker.pose.orientation.x = qx;
    marker.pose.orientation.y = qy;
    marker.pose.orientation.z = qz;
    marker.pose.orientation.w = qw;
    marker.color.a = 1.0
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;
    marker_pub.publish(marker)

if _name_ == '_main_':
    rospy.init_node('movable', anonymous=True)

    pub = rospy.Publisher('pub', PoseStamped, queue_size=10)
    marker_pub = rospy.Publisher('visualization', Marker, queue_size=100)

    rospy.Subscriber('joint_states', JointState, kinematics)

    lines = [line.rstrip('\n') for line in open('../dh', 'r')]

    rospy.spin()

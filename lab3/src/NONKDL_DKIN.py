#! /usr/bin/python

import rospy
import json
import os
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker

def my_listener():
    rospy.init_node('NONKDL_DKIN', anonymous = False)
    rospy.Subscriber("joint_states", JointState , callback)
    rospy.spin()

def callback(data):
    
    main_matrix = translation_matrix((0, 0, 0));
    xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    j = 0
    for i in json_file:
        inst = json.loads(json.dumps(i))
        a = inst["a"]
        d = inst["d"]
        al = inst["alpha"]
        th = inst["theta"]
        trans_z = translation_matrix((0, 0, d * (1 + data.position[j])))
        rot_z = rotation_matrix(th, zaxis)
        trans_x = translation_matrix((a, 0, 0))
        rot_x = rotation_matrix(al, xaxis)

        mat = concatenate_matrices(trans_x, rot_x, rot_z, trans_z)
        main_matrix = concatenate_matrices(main_matrix, mat)
        j=j+1


    x, y, z = translation_from_matrix(main_matrix)
    xq, yq, zq, wq = quaternion_from_matrix(main_matrix)

    robot_pose = PoseStamped()
    robot_pose.header.frame_id = "base_link"
    robot_pose.header.stamp = rospy.Time.now()
    robot_pose.pose.position.x = x
    robot_pose.pose.position.y = y
    robot_pose.pose.position.z = z
    
    robot_pose.pose.orientation.x = xq
    robot_pose.pose.orientation.y = yq
    robot_pose.pose.orientation.z = zq
    robot_pose.pose.orientation.w = wq

    publisher.publish(robot_pose)


if __name__ == '__main__':
    json_file = {}
    publisher = rospy.Publisher('nonKDL_axes', PoseStamped, queue_size=10)

    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
        json_file = json.loads(file.read())

    try:
	    my_listener()        
    except rospy.ROSInterruptException:
        pass

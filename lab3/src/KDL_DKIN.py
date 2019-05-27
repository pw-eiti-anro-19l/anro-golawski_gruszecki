#! /usr/bin/python

import json
import rospy
import PyKDL as kdl
import os
from sensor_msgs.msg import JointState
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped

def my_listener():
    rospy.init_node('KDL_DKIN', anonymous = False)
    rospy.Subscriber("joint_states", JointState , callback)
    rospy.spin()

def callback(data):
    kdlChain = kdl.Chain()   
    createFrame = kdl.Frame();
    d , th = 0 , 0
    j = 1
    for i in json_file:
        inst = json.loads(json.dumps(i))
        d2, th2 = d, th
        a = inst["a"]
        d = inst["d"]
        al = inst["alpha"]
        th = inst["theta"]
        al, a, d, th = float(al), float(a), float(d), float(th)
        if j != 1:
            kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), createFrame.DH(a, al, d2, th2)))
        j = j + 1
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), createFrame.DH(0, 0, d, th)))
      
      
    jointAng = kdl.JntArray(kdlChain.getNrOfJoints())

    jointAng[0] = data.position[0]
    jointAng[1] = data.position[1]
    jointAng[2] = data.position[2]

    fk = kdl.ChainFkSolverPos_recursive(kdlChain)

    last_frame = kdl.Frame()
    fk.JntToCart(jointAng, last_frame)
    quaternion = last_frame.M.GetQuaternion()
    
    robot_pose = PoseStamped()
    robot_pose.header.frame_id = 'base_link'
    robot_pose.header.stamp = rospy.Time.now()

    robot_pose.pose.position.x = last_frame.p[0]
    robot_pose.pose.position.y = last_frame.p[1]
    robot_pose.pose.position.z = last_frame.p[2]

    robot_pose.pose.orientation.x = quaternion[0]
    robot_pose.pose.orientation.y = quaternion[1]
    robot_pose.pose.orientation.z = quaternion[2]
    robot_pose.pose.orientation.w = quaternion[3]
    publisher.publish(robot_pose)
    


if __name__ == '__main__':
    
    json_file = {}
    publisher = rospy.Publisher('kdl_axes', PoseStamped, queue_size=10)

    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
        json_file= json.loads(file.read())
    try:
	    my_listener()        
    except rospy.ROSInterruptException:
        pass
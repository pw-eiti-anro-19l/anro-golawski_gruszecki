#!/usr/bin/env python

import sys
import rospy
from lab4.srv import jint_params

def interpolation_client(x, y, z, time, i):
    rospy.wait_for_service('int')
    try:
        interpolation = rospy.ServiceProxy('int', jint_params)
        resp1 = interpolation(x, y, z, time, i)
        raise Exception('chcesz zagrac w gre?')
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    z = float(sys.argv[3])
    time = float(sys.argv[4])
    i = float(sys.argv[5])
    print "Requesting interpolation"
    print interpolation_client(z, y, x, time, i)

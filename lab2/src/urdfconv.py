#! /usr/bin/python

from tf.transformations import *

x, y, z = (1, 0, 0), (0, 1, 0), (0, 0, 1)

lines = [line.rstrip('\n') for line in open('../dh.txt', 'r')]

file = open('../urdf.yaml', 'w')
with open('../urdf.yaml', 'w') as file:
    i = 1
    for line in lines:
        params = line.split(" ")
        a, d, alfa, theta = params[0], params[1], params[2], params[3]
        a, d, alfa, theta = float(a), float(d), float(alfa), float(theta) #conversion

        trans_z = translation_matrix((0, 0, d))
        rotate_z = rotation_matrix(theta, z)
        trans_x = translation_matrix((0, 0, a))
        rotate_x = rotation_matrix(alfa, x)

        m = concatenate_matrices(trans_z, rotate_z, trans_x, rotate_x)
        rpy_angles = euler_from_matrix(m)
        xyz = translation_from_matrix(m)

        file.write("i" + str(i) + ":\n")
        file.write("  j_xyz: {} {} {}\n".format(*xyz))
        file.write("  j_rpy: {} {} {}\n".format(*rpy_angles))
        file.write("  l_xyz: {} 0 0\n".format(xyz[0] / 2))
        file.write("  l_rpy: 0 0 0\n")
        file.write("  l_len: {}\n".format(a))
        i += 1

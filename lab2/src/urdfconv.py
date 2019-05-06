#! /usr/bin/python
import json
from tf.transformations import *



if __name__ == '__main__':
    xaxis = (1,0,0)
    yaxis = (0,1,0)
    zaxis = (0,0,1)
    params = {}
    with open('../dh.json', 'r') as file:
        params=json.loads(file.read())

    with open('../urdf.yaml', 'w') as file:
        for param in params:
            inst = json.loads(json.dumps(param))
            a = inst["a"]
	    d = inst["d"]
	    al = inst["alpha"]
	    th = inst["theta"]

            trans_z = translation_matrix((0,0,d))
            rot_z = rotation_matrix(th, zaxis)
            trans_x = translation_matrix((a,0,0))
            rot_x = rotation_matrix(al, xaxis)

            mat = concatenate_matrices(trans_x, rot_x, rot_z, trans_z)

            (roll, pitch, yaw) = euler_from_matrix(mat)
            (x,y,z) = translation_from_matrix(mat)

            file.write(inst["name"] + ":\n")
            file.write("    j_xyz: " + str(x) + " " + str(y) + " "+ str(z) + "\n")
            file.write("    j_rpy: " + str(roll) + ' '+str(pitch) + ' ' + str(yaw) + "\n")
            file.write("    l_xyz: " + str(0) + ' ' + str(0) + ' ' + str(float(d)*(-0.5)) + "\n")
            file.write("    l_rpy: " + str(0) + ' ' + str(0) + ' ' + str(0) + "\n")
            file.write("    l_len: " + str(d) + "\n")

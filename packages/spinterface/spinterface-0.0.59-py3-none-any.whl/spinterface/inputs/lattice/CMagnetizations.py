import numpy as np
from spinterface.inputs.lattice.utilities import rotate_spins,rotation_matrix

class Magnetisation_Domainwall():
    def __init__(self, X, Y, r0, direction, width, heli):
        self.mx, self.my, self.mz = self.build_domainwall(X, Y, r0, direction, width, heli)

    def build_domainwall(self, X, Y, r0, direction, width, heli):
        mx, my, mz = [], [], []
        direction = np.asarray(direction)/np.linalg.norm(direction)
        R0 = np.absolute(direction)*r0
        # construct axis for rotation:
        axismat = rotation_matrix([0.0, 0.0, 1.0], heli)
        axis = rotate_spins([direction[0]], [direction[1]], [0.0], axismat)
        axis = np.asarray([axis[0][0], axis[1][0], axis[2][0]])
        # rotate every spin with own matrix according to @theta and @axis
        # the angle theta is given by the DW profile
        for n in range(len(X)):
            r = np.asarray([X[n], Y[n]])
            arg = np.dot(r-R0, direction)/width
            theta = 2.0*np.arctan(np.exp(arg))
            mat = rotation_matrix(axis, theta)
            mag = rotate_spins([0.0] ,[0.0], [1.0], mat)
            mx.append(mag[0][0])
            my.append(mag[1][0])
            mz.append(mag[2][0])
        return mx, my, mz

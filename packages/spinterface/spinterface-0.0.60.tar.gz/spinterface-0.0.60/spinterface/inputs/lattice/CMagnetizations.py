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

class Magnetisation_Bimeron():
    def __init__(self, X, Y, pos0, R, a1, a2):
        self.mx, self.my, self.mz = self.build_bimeron(X, Y, pos0, R, a1, a2)

    #===============================================
    #magnetisation direction in spherical coordinates
    #===============================================
    def theta(self, R, c_i, c_j, a1, a2):
        rho = np.sqrt(a1*c_i**2 + a2*c_j**2)
        return np.arccos(R * c_i / (rho**2 + (R**2)/4 ))

    def phi(self, R, c_i, c_j):
        return np.arctan((c_i - R/2)/(c_j)) - np.arctan((c_i + R/2)/(c_j))

    def build_bimeron(self, X, Y, pos0, R, a1, a2):
        r = 1
        assert len(X) == len(Y)
        mx, my, mz = np.zeros(len(X)), np.zeros(len(X)), np.zeros(len(X))
        for n in range(len(X)):
            theta_c = self.theta(R, X[n]-pos0[0], Y[n]-pos0[1], a1, a2)
            phi_c   = self.phi(R, X[n]-pos0[0], Y[n]-pos0[1])
            mx[n] = np.round(r*np.sin(theta_c)*np.cos(phi_c),8)
            my[n] = np.round(r*np.sin(theta_c)*np.sin(phi_c),8)
            mz[n] = np.round(r*np.cos(theta_c),8)
        return mx, my, mz


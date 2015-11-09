import numpy as np
import scipy.interpolate as scinterp
import matplotlib.pyplot as plt

class Optimizer(object):
    def __init__(self, mjd, mag, error, spline, guess):
        self.mjd = mjd
        self.mag = mag
        self.error = error
        self.spline = spline
        self.guess = guess

    def GOF(self, x):
        if x < 0: x = 0 
        print x
        nknots = self.guess
        
        tck = scinterp.splrep(self.mjd, self.mag, 1/self.error,
             k = 3, t = knots)
        newMag = scinterp.splev(self.mjd, tck)
        

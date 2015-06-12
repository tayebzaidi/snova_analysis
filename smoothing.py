import numpy as np
import scipy.interpolate 
import sys

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def find_nearest_ind(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def UnivariateSplinefit(x,y,z):
    s = scipy.interpolate.UnivariateSpline(x,y)
    s.set_smoothing_factor(z)
    return s(x)

def Interpolate1D(x, y):
    s = scipy.interpolate.interp1d(x,y)
    return s 

def MvB(mag, phase, minpts):
    if len(minpts) > 2 or len(minpts) == 0:
        pass
    else:
        return minpts[0][1]


def delM15(mag_func,phase, minpts):
    if len(minpts) != 0 and len(minpts) < 3:
        magnitude_at_15 = mag_func(minpts[0][0]+15)
        delM15val =  magnitude_at_15  - minpts[0][1] 
        return delM15val

def SmoothingFactor():
    pass

if __name__=='__main__':
    sys.exit()


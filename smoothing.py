from scipy.interpolate import UnivariateSpline
import sys

def UnivariateSplinefit(x,y,z):
    s = UnivariateSpline(x,y)
    s.set_smoothing_factor(z)
    return s(x)

def SmoothingFactor():
    pass

if __name__=='__main__':
    sys.exit()


import matplotlib.pyplot as plt
import numpy as np
import peakfinding
import smoothing
import plotter
import readin
import sys

if __name__== '__main__':
    #lcurve = readin.readin_aavso('aavsodata_sscyg.txt')
    #mjd = lcurve.jd - 240000.5
    #mag = lcurve.magnitude
    #maxtab, mintab = peakfinding.peakdet(mag,1.2 , mjd)
    #smoothed = smoothing.UnivariateSplinefit(mjd, mag,5)
    #maxtab, mintab = peakfinding.peakdet(smoothed, 1, mjd)
    #data = readin.readin_SNANA('CFA4_2006ct.dat')
    #plotter.plot1D(mjd, smoothed, 'blue', 0,1) 
    #plotter.plot1D(mjd, mag, 'red', 1,1)
    #plotter.Show()
    data = readin.readin_SNrest('SN1972E.rest.dat')
    print data.phase, data.mag
    ax = plotter.plot1D(data.phase, data.mag,'blue',1) 
    plotter.plot1D(data.phase, data.mag+ 1, 'red',1, lnstyle = "-")
    plotter.Show()
    #plt.plot(data.phase, data.mag, linestyle = ':')
    #plt.gca().invert_yaxis()
    #plt.show()

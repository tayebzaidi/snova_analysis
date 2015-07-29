#!/usr/bin/env python
import matplotlib.pyplot as plt
import scipy.interpolate as scinterp
import scipy.signal
from scipy.ndimage import filters
import numpy as np
import peak_original
import sys
import random
import os

def moving_average(series, sigma=0.7):
    b = scipy.signal.gaussian(39, sigma)
    average = filters.convolve1d(series, b/b.sum())
    var = filters.convolve1d(np.power(series-average,2), b/b.sum())
    return average, var

#_, var = moving_average(series)
#sp = ip.UnivariateSpline(x, series, w=1/np.sqrt(var))

def readinSNANA(filename, path = "/Users/zaidi/Documents/REU/SNDATA/lcmerge/CFA3_KEPLERCAM"):
    lookup = 'NVAR'
    linenum = 16
    with open(os.path.join(path,filename), 'r') as lcurvefile:
        for num, line in enumerate(lcurvefile):
            if lookup in line:
                linenum = num    
    formatcode = ('|S16,'.rstrip(':') + 'f8,'+ '|S16,'*2 + 'f8,'*4 )
    data = np.recfromtxt(os.path.join(path, filename), dtype = None, names = True, skip_header = linenum + 1, skip_footer = 1,case_sensitive = "lower", invalid_raise = False)
    return data


def readinSNANA_hz(filename):
   pass 


def main():
    path = "/Users/zaidi/Documents/REU/SNDATA/lcmerge/CFA3_KEPLERCAM/"
    #filename = raw_input("Enter filename: ")
    
    try:
        filename = sys.argv[1]
    except IndexError:
        filenames = os.listdir(path)
        random.shuffle(filenames)
        filename = filenames[1]
    
    featuredat = {filename : {}}

    data = readinSNANA(filename)
    days_after_peak = 15
    #band1 = raw_input("Enter band 1:  ")
    #band2 = raw_input("Enter band 2:  ")
    #band1 = 'I'
    filters = ['B', 'V', 'R', 'I', 'U']
    for flter in filters:
        indb1 = np.where((data.flt == flter))
        b1data = data[indb1]
        #b1data = np.sort(b1data, axis = 1)
        #b2data = np.sort(b2data, axis = 1)
        if len(b1data.mjd) > 3:
            
            #_, var = moving_average(b1data.mag)
            #splb1 = scinterp.UnivariateSpline(b1data.mjd, b1data.mag, w=1/np.sqrt(var))
            #print 1/np.sqrt(var)
            splb1 = scinterp.UnivariateSpline(b1data.mjd, b1data.mag)
            splb1.set_smoothing_factor(0.4/len(b1data.mag))
            phase_new = np.linspace(b1data.mjd[0], b1data.mjd[-1], num = 1 * len(b1data.mjd))
            mag_newb1 = splb1(phase_new)
            maxp, minp = peak_original.peakdet(splb1(phase_new), 0.06, phase_new)
            print minp
            print filename
            fig = plt.figure(figsize = (12,12))
            ax = fig.add_subplot(1,1,1)
            ax.plot(phase_new, mag_newb1)
            ax.plot(b1data.mjd, b1data.mag, color = 'blue', alpha = 0.6)
            if len(minp) > 0:
                ax.scatter(minp[:,0], minp[:,1])
            plt.show(fig)
            if len(minp) > 0 and len(minp) < 2 and minp[0][0] < (b1data.mjd[0] + 35):
                featuredat[filename][flter] = [minp[0][0], minp[0][1],'nan','nan','nan', float(splb1(minp[0][0] + days_after_peak))]
            elif len(minp) > 0 and len(minp) > 1 and minp[1][0] < (minp[0][0] + 65):
                featuredat[filename][flter] = [minp[0][0], minp[0][1], minp[1][0], minp[1][1], minp[1][0]-minp[0][0], float(splb1(minp[1][0] + days_after_peak))]
            else:
                featuredat[filename][flter] = ['nan', 'nan','nan','nan','nan', 'nan']
            print featuredat
        else:
            featuredat[filename][flter] = ['nan', 'nan','nan', 'nan','nan','nan']
            print 'insufficient data'
            print filename
    










if __name__ == "__main__":
    sys.exit(main())

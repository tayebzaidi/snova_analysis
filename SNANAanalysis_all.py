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
import json
import glob
from supersmoother import SuperSmoother

def readin(filename, path):
    if '.rest.dat' in filename:
        data = readin_SNrest(filename)
        return data
    else:
        data = readinSNANA(filename, path)

def readin_SNrest(filename):
    path = "/Users/zaidi/Documents/REU/restframe/"
    formatcode = ('|S16,'.rstrip('#') +'f8,'*6 + '|S16,' + 4 * 'f8,' + '|S16,' * 3 + 'f8,' * 2 + '|S16,' + 'f8,' * 2)
    data = np.recfromtxt(os.path.join(path, filename),usecols = (0,1,2,3,4), dtype = formatcode, names = True, skip_header = 13, case_sensitive = 'lower', invalid_raise = False)
    #ind = np.where(np.logical_or(data.band == 'B', data.band == 'V') & (data.err < 0.2))
    #banddata = data[ind]
    return data

def moving_average(series, sigma=0.7):
    b = scipy.signal.gaussian(39, sigma)
    average = filters.convolve1d(series, b/b.sum())
    var = filters.convolve1d(np.power(series-average,2), b/b.sum())
    return average, var

#_, var = moving_average(series)
#sp = ip.UnivariateSpline(x, series, w=1/np.sqrt(var))

def readinSNANA(filename, path = "/home/tensortrash/Development/REU/hack_day/lcmerge/CFA3_KEPLERCAM/"):
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
    path = "/home/tensortrash/Development/REU/hack_day/lcmerge/CFA3_KEPLERCAM/"
    #filename = raw_input("Enter filename: ")
    filenames = []
    for name in glob.glob("/home/tensortrash/Development/REU/hack_day/lcmerge/*/*.dat"):
        filenames.append(name)
    for name in glob.glob("/home/tensortrash/Development/REU/hack_day/lcmerge/*/*.DAT"):
        filenames.append(name)
    splinedat = [{}]
    for path_complete in filenames:
        head, tail = os.path.split(path_complete)
        #print tail
        data = readinSNANA(tail, head)
        days_after_peak = 15
        #band1 = raw_input("Enter band 1:  ")
        #band2 = raw_input("Enter band 2:  ")
        #band1 = 'I'
        filters = list(set(data.flt))
        for flter in filters:
            indb1 = np.where((data.flt == flter))
            b1data = data[indb1]
            #b1data = np.sort(b1data, axis = 1)
            #b2data = np.sort(b2data, axis = 1)
            
            if len(b1data.mjd) > 9:
               
                #_, var = moving_average(b1data.mag)
                #splb1 = scinterp.UnivariateSpline(b1data.mjd, b1data.mag, w=1/np.sqrt(var))
                #print 1/np.sqrt(var)
                splb1 = scinterp.UnivariateSpline(b1data.mjd, b1data.mag)
                splb1.set_smoothing_factor((len(b1data.mag) - (len(b1data.mag)*2)**0.5)*0.05*0.05)
                phase_new = np.linspace(b1data.mjd[0], b1data.mjd[0] + 20, num = 20)
                mag_newb1_tmp = splb1(phase_new).tolist()
                maxp, minp = peak_original.peakdet(mag_newb1_tmp, 0.06, phase_new)
                
                if len(minp) > 0:
                    b1data.mag = b1data.mag - minp[0][1]
                else:
                    b1data.mag = b1data.mag - b1data.mag[0] 
                splb1 = scinterp.UnivariateSpline(b1data.mjd, b1data.mag)
                splb1.set_smoothing_factor((len(b1data.mag) - (len(b1data.mag)*2)**0.5)*0.05*0.05)
                mag_newb1 = splb1(phase_new)
                '''
                fig = plt.figure(figsize = (12,12))
                ax = fig.add_subplot(1,1,1)
                ax.plot(phase_new, mag_newb1)
                ax.plot(b1data.mjd, b1data.mag, color = 'blue', alpha = 0.6)
                #if len(minp) > 0:
                #    ax.scatter(minp[:,0], minp[:,1])
                plt.show(fig)
                '''
                something = np.isnan(mag_newb1)
                if len(something[something == 1]) == 0 and mag_newb1.max() < 10 and mag_newb1.min() > -5:
                    splinedat.append({'id': tail, 'band': flter, 'splinedata': mag_newb1.tolist()})
                '''
                if len(minp) > 0 and len(minp) < 2 and minp[0][0] < (b1data.mjd[0] + 35) and minp[0][0] > 0:
                    featuredat.append({'id': tail, 'band': flter, 'mins':[minp[0][1],float('NaN')], 't': [float('NaN')], 'delta_m': [splb1(minp[0][0] + days_after_peak) - minp[0][0]]})
                elif len(minp) > 0 and len(minp) > 1 and minp[1][0] < (minp[0][0] + 30) and minp[0][0] > 0:
                    featuredat.append({'id': tail, 'band': flter, 'mins':[minp[0][1],minp[1][1]], 't': [minp[1][0] - minp[0][0]], 'delta_m': [splb1(minp[1][0] + days_after_peak) - minp[1][0]]})
                elif len(minp) > 0 and len(minp) > 1 and minp[0][0] > 0:
                    featuredat.append({'id': tail, 'band': filters, 'mins':[minp[0][1],float('NaN')], 't': [float('NaN')], 'delta_m': [splb1(minp[0][0] + days_after_peak) - minp[0][0]]})
                else:
                    featuredat.append({'id': tail, 'band': flter, 'mins':[float('NaN'),float('NaN')], 't': [float('NaN')], 'delta_m': [float('NaN')]})
            else:
                featuredat.append({'id': tail, 'band': flter, 'mins':[float('NaN'),float('NaN')], 't': [float('NaN')], 'delta_m': [float('NaN')]})
    
                #print 'insufficient data'
                #print filename
                '''
                '''
                #if len(minp) > 0 and len(maxp) > 0:
                #    b1data.mjd = maxp[-1][1] - maxp
                 
                model = SuperSmoother()
                model.fit(b1data.mjd, b1data.mag, b1data.magerr)
                
                x = np.linspace(b1data.mjd[0], b1data.mjd[-1], num = 20).tolist()
                y_tmp = model.predict(x).tolist()
                maxp, minp = peak_original.peakdet(y_tmp, 0.08, x)
                if len(minp) > 0:
                    b1data.mag = b1data.mag - minp[0][1]
                else:
                    b1data.mag = b1data.mag - b1data.mag[0]

                model.fit(b1data.mjd, b1data.mag, b1data.magerr)
                y = model.predict(x).tolist()
                splinedat.append({'id': tail, 'band': [flter], 'splinedata': y})
                fig = plt.figure()
                ax = fig.add_subplot(1,1,1)
                ax.plot(x, y)
                ax.scatter(b1data.mjd, b1data.mag, color = 'blue', alpha = 0.6)
                if len(minp) > 0:
                    ax.scatter(minp[:,0], minp[:,1])
                plt.show(fig)
                '''

    f_out = open('SplineData', 'w')
    f_out.write(json.dumps(splinedat, sort_keys=True, indent=4))
    f_out.close()
    #print splinedat

                # plt.plot(x, model.predict(x))
                # plt.scatter(xdata, ydata)
                # plt.show()
    '''                    
                print splinedat 
                with open('FeatureJSON', 'w') as outfile:
                    json.dumps(featuredat, outfile)
    '''








if __name__ == "__main__":
    sys.exit(main())

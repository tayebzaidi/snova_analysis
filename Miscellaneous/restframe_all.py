#!/usr/bin/env python
import matplotlib.pyplot as plt
import scipy.interpolate as scinterp
import scipy.signal
from scipy.ndimage import filters
import numpy as np
import peak_original
import peakfinding
import sys
import random
import os
import json
import glob

import matplotlib as mpl

mpl.rcParams['axes.linewidth'] = 2 #set the value globally

def find_nearest_ind(array,value):
    idx = np.abs(array-value).argmin()
    return idx

def readin_SNrest(filename):
    path = "/Users/zaidi/Documents/REU/restframe/"
    formatcode = ('|S16,'.rstrip('#') +'f8,'*6 + '|S16,' + 4 * 'f8,' + '|S16,' * 3 + 'f8,' * 2 + '|S16,' + 'f8,' * 2)
    data = np.recfromtxt(os.path.join(path, filename),usecols = (0,1,2,3,4), dtype = formatcode, names = True, skip_header = 13, case_sensitive = 'lower', invalid_raise = False)
    return data

def readin_lcstandard_harvard():
    path = '/Users/zaidi/Downloads/lc.standardsystem.sesn_allphot.dat'
    formatcode = ('|S16,' + '|S16,' + 'f8,' * 3 + '|S16,')
    data = np.recfromtxt(path, dtype = formatcode, names = ['filename', 'flt', 'mjd', 'mag', 'magerr', 'survey'], case_sensitive = 'lower', invalid_raise = False)
    data.flt = np.array([x.replace('prime','',1) for x in data.flt.tolist()])
    return data

def main():
    splinedat = [{}]
    data = readin_lcstandard_harvard()
    B_band_offset = 0
    filenames = list(set(data.filename))
    random.shuffle(filenames)
    try:
        pass
        #filenames = []
    except:
        pass
    for filename in filenames:
        print filename, "\t"
        filters = list(set(data.flt))
        idx = np.where((np.array(filters) == 'B'))
        print idx
        filters.insert(0, filters.pop(idx[0])) #Move B band to front of filters array
        print filters
        for flter in filters:
            ind = np.where((data.flt == flter) & (data.filename == filename))
            banddata = data[ind]
            if len(banddata.mjd) > 6:
                order = np.argsort(banddata.mjd)
                mjd_sampled_ind = np.arange(2, find_nearest_ind(banddata.mjd[order], banddata.mjd.min() + 25), 7)
                sparse =  np.arange(find_nearest_ind(banddata.mjd, banddata.mjd.min() + 25), find_nearest_ind(banddata.mjd, banddata.mjd.max()), 10)
                idx_final = np.append(mjd_sampled_ind, sparse)
                mjd_sampled = banddata.mjd[idx_final]
                
                mjd_new = np.linspace(banddata.mjd.min(), banddata.mjd.max(), num = 200)
                spl1d = scinterp.interp1d(banddata.mjd[order], banddata.mag[order])
                maxp, minp = peakfinding.peakdetect(spl1d(mjd_new), mjd_new, 10, 0.03)
                
                minp = np.array(minp)
                maxp = np.array(maxp)
                mag_knot = []
                minp3 = []
                maxp3 = []

                if len(minp) > 0 and minp[0][0] < (banddata.mjd.min() + 25) and minp[0][0] > banddata.mjd.min():
                    
                                            
                    print flter
                        
                    tck = scinterp.splrep(banddata.mjd[order], banddata.mag[order], t = mjd_sampled, w = 1./(banddata.magerr)**2)
                    mag_knot = scinterp.splev(mjd_new, tck)
                    maxp3, minp3 = peakfinding.peakdetect(mag_knot, mjd_new, 20, 0.1)
                    
                    mjd_20 = np.linspace(banddata.mjd[order].min(), banddata.mjd[order].min() + 40, num = 30)
                    splinedata = scinterp.splev(mjd_20, tck)

                    #phase correction
                        
                    mjd_20 = mjd_20 - minp[0][0]
                        
                    #magnitude correction
                    splinedata = splinedata - banddata.mag.min()
                                    
    
                    splinedat.append({'id': filename, 'dataset': 2, 'band': flter, 'splinedata': splinedata.tolist(), 'phase': mjd_20.tolist()})
                

                #fig = plt.figure(figsize = (12,12))
                #ax = fig.add_subplot(1,1,1)
                #if len(mjd_new) == len(mag_knot):
                #    ax.plot(mjd_new, mag_knot, color = 'green')
                #ax.plot(banddata.mjd[order], spl1d(banddata.mjd[order]))
                #ax.scatter(banddata.mjd, banddata.mag, color = 'blue')
                #plt.draw()
                #plt.pause(0.1)
                #a = raw_input("<Hit key to close>")
                #if a == 's':
                #    f.write("%s \n" % filename)
                #    plt.close(fig)
                #    break
                #elif a =='q':
                #    f.close()
                #    sys.exit()
                #plt.close(fig)
    #f.close()
    main2(splinedat)


def main2(splinedat):
    try:
        filenames =  [sys.argv[1]]
        prnt = False
    except:
        prnt = False
        path = "/Users/zaidi/Documents/REU/restframe/"
        filenames = os.listdir(path)
        random.shuffle(filenames)
        prnt = True
    for filename in filenames:
        print filename
        data = readin_SNrest(filename)
        filters = list(set(data.band))
        for flter in filters:
            ind = np.where(data.band == flter)
            banddata = data[ind]

            if len(banddata.phase) > 10:
               
                order = np.argsort(banddata.phase)
                phase_sampled_ind = np.arange(2, find_nearest_ind(banddata.phase[order], banddata.phase.min() + 25), 7)
                sparse = np.arange(find_nearest_ind(banddata.phase[order], banddata.phase.min() + 25), find_nearest_ind(banddata.phase[order], banddata.phase.max()), 10)
                idx_final = np.append(phase_sampled_ind, sparse) #connect wellsampled and sparse indices
                phase_sampled = banddata.phase[order][idx_final]

                phase_new = np.linspace(banddata.phase.min(), banddata.phase.max(), num = 200) # generate new phase data to sample at
                
                spl1d = scinterp.interp1d(banddata.phase[order], banddata.mag[order])
                maxp, minp = peakfinding.peakdetect(spl1d(phase_new), phase_new, 10, 0.03)
                minp = np.array(minp)
                maxp = np.array(maxp)
                mag_knot = []
                minp3 = []
                maxp3 = []
    
                if len(minp) > 0 and minp[0][0] < 10 and minp[0][0] > -10:
                    print banddata.phase
                    print phase_sampled
                    try:
                        tck = scinterp.splrep(banddata.phase[order], banddata.mag[order], t = phase_sampled, w = 1./(banddata.err[order])**2)
                    except:
                        pass
                    mag_knot = scinterp.splev(phase_new, tck)
                    maxp3, minp3 = peakfinding.peakdetect(mag_knot, phase_new, 10, 0.1)
                    minp3 = np.array(minp3)
                    maxp3 = np.array(maxp3) 
                                        
                    phase_20 = np.linspace(banddata.phase.min(), banddata.phase.min() + 40, num = 30)
                    splinedata = scinterp.splev(phase_20, tck)

                    #magnitude correction
                    splinedata = splinedata - banddata.mag.min()
    
                    splinedat.append({'id': filename, 'data': 1,'band': flter, 'splinedata': splinedata.tolist(), 'phase': phase_20.tolist()})
                #t = minp[:,0]
                #spl.set_smoothing_factor(0.1)
                #mag_new = spl(phase_new)
                #maxp, minp = peak_original.peakdet(mag_new, 0.06, phase_new)
                
                '''
                if len(minp) > 0:
                    banddata.mag = banddata.mag - minp[0][1]
                    banddata.mag = banddata.mag / float(banddata.mag.max())
                else:
                    banddata.mag = banddata.mag - banddata.mag[0]
                spl = scinterp.UnivariateSpline(banddata.phase, banddata.mag)
                spl.set_smoothing_factor(0.01)
                mag_new = spl(phase_new)
                print spl(phase_new[1])
                '''
                
                if prnt == True:
                    fig = plt.figure(figsize = (12,12))
                    ax = fig.add_subplot(1,1,1)
                    if len(phase_new) == len(mag_knot):
                        ax.plot(phase_20, splinedata, color = 'green', lw = 3)
                    ax.errorbar(banddata.phase[order], spl1d(banddata.phase[order]) - banddata.mag.min(), yerr = banddata.err[order], fmt = 'o', ms = 5)
                    ax.text(35, 0, filename.rstrip('.rest.dat'), fontsize = 18)
                    ax.set_xlabel('Phase (days)', fontsize = 18)
                    ax.set_ylabel('Magnitude', fontsize = 18)
                    ax.scatter(banddata.phase, banddata.mag - banddata.mag.min(), color = 'brown', alpha = 0.4)
                    if len(minp) > 0:
                        ax.scatter(minp[:,0], minp[:,1] - banddata.mag.min(), color = 'red')
                    if len(minp3):
                        ax.scatter(minp3[:,0], minp3[:,1] - banddata.mag.min(), color = 'red')
                    if len(maxp) > 0:
                        ax.scatter(maxp[:,0], maxp[:,1] - banddata.mag.min(), color = 'blue')
                    if len(maxp3) > 0:
                        ax.scatter(maxp3[:,0], maxp3[:,1] - banddata.mag.min(), color = 'blue')
                        
                    plt.gca().invert_yaxis()
                    plt.show(fig)
                    
    
    f_out = open('SplineDatarestImproved', 'w')
    f_out.write(json.dumps(splinedat, sort_keys=True, indent=4))
    f_out.close()



if __name__ == '__main__':
    sys.exit(main())

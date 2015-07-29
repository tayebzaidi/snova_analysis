import matplotlib.pyplot as plt
import scipy.interpolate as scinterp
import numpy as np
import peakfinding
import peak_original
import smoothing
import plotter
import random
import readin
import sys
import os

if __name__== '__main__':
    Mbdata = []
    delM15data = []
    path = "/Users/zaidi/Documents/REU/restframe/"
    filenames = os.listdir(path)
    random.shuffle(filenames)
    for filename in filenames:
        current_file = os.path.join(path, filename)
        data= readin.readin_SNrest(filename)
        indB = np.where((data.band == 'B'))
        Bdata = data[indB]
        Bdata = np.sort(Bdata)
        if len(Bdata.phase) > 3:
            spl = scinterp.UnivariateSpline(Bdata.phase, Bdata.mag)
            spl.set_smoothing_factor(2./len(Bdata.phase))
            phase_new = np.arange(Bdata.phase[0], Bdata.phase[-1], 1)
            mag_new = spl(phase_new)
            maxp, minp = peak_original.peakdet(mag_new, 0.5, phase_new)
            if len(minp) > 0 and minp[0][0] < 5 and minp[0][0] > -5:
                Mb = minp[0][1]
                delM15 = minp[0][1] - spl(minp[0][0]+15)
                Mbdata.append(Mb)
                delM15data.append(delM15) 
                if delM15 > 0 or delM15 < -5:
                    print minp
                    print filename
                    print spl(minp[0][0] + 15)
                    fig = plt.figure(1)
                    ax = fig.add_subplot(1,1,1)
                    ax.plot(phase_new, mag_new)
                    ax.plot(Bdata.phase, Bdata.mag)
                    if len(minp) > 0:
                        ax.scatter(minp[:,0],minp[:,1])
                    plt.show(fig)
        
        '''
        maxp, minp = peakfinding.peakdetect(mag_new, phase_new, 200, 1.5)
        if len(minp) > 0:
            print minp
            print filename
            fig = plt.figure(1)
            ax = fig.add_subplot(1,1,1)
            #ax.scatter(minp[:,0], minp[:,1],'bo')
            #ax.plot(Bdata.phase, Bdata.mag)
            #plt.show(fig) 
        
        '''
        #interp = smoothing.Interpolate1D(data.phase
    print Mbdata
    print delM15data
    fig = plt.figure(2)
    ax = fig.add_subplot(1,1,1)
    ax.scatter(Mbdata, delM15data)
    plt.show(fig)

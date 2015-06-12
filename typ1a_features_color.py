import matplotlib.pyplot as plt
from matplotlib import gridspec
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
    hist_at_20 = []
    path = "/Users/zaidi/Documents/REU/restframe/"
    filenames = os.listdir(path)
    random.shuffle(filenames)
    for filename in filenames:
        current_file = os.path.join(path, filename)
        data= readin.readin_SNrest(filename)
        indB = np.where((data.band == 'B'))
        indV = np.where((data.band == 'V'))
        Bdata = data[indB]
        Vdata = data[indV]
        Vdata = np.sort(Vdata)
        Bdata = np.sort(Bdata)
        
        if len(Bdata.phase) > 5 and len(Vdata.phase) > 5:
            splB = scinterp.UnivariateSpline(Bdata.phase, Bdata.mag)
            splV = scinterp.UnivariateSpline(Vdata.phase, Vdata.mag)
            splV.set_smoothing_factor(04./len(Vdata.phase))
            splB.set_smoothing_factor(04./len(Bdata.phase))
            phase_newB = np.arange(Bdata.phase[0], Bdata.phase[-1], 1)
            mag_newB  = splB(phase_newB)
            mag_newV  = splV(phase_newB)
            color_mag = mag_newB - mag_newV
            splC = scinterp.UnivariateSpline(phase_newB, color_mag)
            splC.set_smoothing_factor(04/len(Bdata.phase))
            maxp, minp = peak_original.peakdet(splC(phase_newB), 0.08, phase_newB )

            
            '''
            fig3 = plt.figure(3)
            ax = fig3.add_subplot(1,1,1)
            ax.plot(Bdata.phase, color_mag)
            #ax.plot(Bdata.phase, Bdata.mag)
            plt.show()
            a = raw_input("Waiting")
            '''
            if len(minp) > 0 and minp[0][0] < 5 and minp[0][0] > -5:
                Mb = minp[0][1]
                delM15 = minp[0][1] - splC(minp[0][0]+15)
                Mbdata.append(Mb)
                delM15data.append(delM15)
                hist_at_20.append(splC(minp[0][0]+20))
                print minp
                print filename
                print splB(minp[0][0] + 15)
                #fig = plt.figure(1)
                #ax = fig.add_subplot(1,1,1)
                #ax.plot(phase_newB, splC(phase_newB))
                
                if len(minp) > 0:
                    #ax.scatter(minp[:,0],minp[:,1])
                    pass
                #plt.show(fig)

    fig = plt.figure(2)
    #ax = fig.subplot(1,1,1)
    #ax.scatter(delM15data, Mbdata)
    ax2 = fig.add_subplot(1,1,1)
    ax2.hist(hist_at_20)
    #ax.gca().invert_yaxis()
    #ax.gca().invert_xaxis()
    plt.show(fig)





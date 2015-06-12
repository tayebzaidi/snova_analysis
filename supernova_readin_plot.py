import matplotlib.pyplot as plt
import numpy as np
import peakfinding
import smoothing
import plotter
import readin
import sys
import os

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
    #data = readin.readin_SNrest()
    #maxp, minp = peakfinding.peakdet(data.mag, 1, data.phase)
    #interp = smoothing.Interpolate1D(data.phase, data.mag)
    path = "/Users/zaidi/Documents/REU/restframe/"
    Mvbdata = []
    delM15data = []
    err_data = []
    for filename in os.listdir(path):
        current_file = os.path.join(path, filename)
        data= readin.readin_SNrest(filename)
        try:
            interp = smoothing.Interpolate1D(data.phase, data.mag)
            maxp, minp = peakfinding.peakdet(data.mag, 0.55, data.phase)
            Mvb = smoothing.MvB(data.mag, data.phase, minp)
            delM15 = smoothing.delM15(interp, data.phase, minp)
            if len(minp) != 0 and len(minp) < 3:
                Mvbdata.append(Mvb)
                delM15data.append(delM15)
                err_data.append(data.err)
                ''' 
                fig = plt.figure(figsize=(6,6))
                ax = fig.add_subplot(1,1,1)
                ax.plot(data.phase, data.mag, 'k.', [minp[0][0]+15], interp(minp[0][0]+15), 'bo')
                ax.axvline(minp[0][0])
                ax.axvline(minp[0][0]+15)
                ax.axhline(interp(minp[0][0]+15))
                ax.axhline(minp[0][1])
                plt.savefig(filename + '.png')
                '''
        except ValueError:
            print filename, data
            print data.mag, data.phase
            print (len(data.mag), len(data.phase)) 
        
        ''' 
        print interp(15)
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(1,1,1)
        ax.plot(data.phase, data.mag, 'k.', [15.], interp(15), 'bo')
        plt.ion()
        plt.show(fig)
        '''
        
        
        
        #sys.exit(-1)
        ''' 
        ax = plotter.plot1D(data.phase, interp,'blue',1, lnstyle = '-') 
        try:
            plotter.plot1DScatter(minp[:,0], minp[:,1], 'red', 1) 
        except IndexError:
            pass
        plotter.Show()
        plotter.Clear()
        a = raw_input("Press Enter to continue...")
        if a == "q":
            break
        '''
    
    fig2 = plt.figure(2)
    ax = fig2.add_subplot(1,1,1)
    ax.scatter(Mvbdata, delM15data,)
    ax2 = fig2.add_subplot(3,2,1)
    ax2.hist(err_data, 5)
    plt.show(fig2)
    
    #plt.plot(data.phase, data.mag, linestyle = ':')
    #plt.gca().invert_yaxis()
    #plt.show()

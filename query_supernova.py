import matplotlib.pyplot as plt
import scipy.interpolate as scinterp
import numpy as np
import peak_original
import readin
import sys
import os


def main():
    #path = '/Users/zaidi/Documents/REU/SNDATA/lcmerge/CFA3_KEPLERCAM/'
    filename = raw_input("Enter file name:  ")
    band1 = raw_input("Enter band 1:  ")
    band2 = raw_input("Enter band 2:  ")
    path_to = os.path.join(path, filename)
    
def SNANA(path_to, band1, band2):
    data = readin.readin_SNANA(filename


def SN_rest(filename, band1, band2):
    data = readin.readin_SNrest(path_to, band1, band2)
    indb1 = np.where((data.band == band1))
    indb2 = np.where((data.band == band2))
    b1data = data[indb1]
    b2data = data[indb2]
    b1data = np.sort(b1data)
    b2data = np.sort(b2data)
    
    if len(b1data.phase) > 5 and len(b2data.phase) > 5:
        splb1 = scinterp.UnivariateSpline(b1data.phase, b1data.mag)
        splb2 = scinterp.UnivariateSpline(b2data.phase, b2data.mag)
        splb1.set_smoothing_factor(04./len(b1data.phase))
        splb2.set_smoothing_factor(04./len(b2data.phase))
        phase_new = np.arange(b2data.phase[0], b2data.phase[-1], 1)
        mag_newb1 = splb1(phase_new)
        mag_newb2 = splb2(phase_new)
        color_mag = mag_newb1 - mag_newb2
        splC = scinterp.UnivariateSpline(phase_new, color_mag)
        splC.set_smoothing_factor(04./len(b1data.phase))
        maxp, minp = peak_original.peakdet(splC(phase_new), 0.08, phase_new)
        phase_inp = float(raw_input("Enter phase at which you want color information:  "))
        print b1data
        print b2data
        if len(minp) > 0:
            Mb = minp[0][1]
            color_at_inp = splC(phase_inp)
            print path
            print Mb
            print color_at_inp
        else:        
            pass
        color_at_inp = splC(phase_inp)
        print color_at_inp
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.plot(phase_new, splC(phase_new))
        if len(minp) > 0:
            ax.scatter(minp[:,0], minp[:,1])
        plt.show(fig)
        









if __name__ == "__main__":
    sys.exit(main())

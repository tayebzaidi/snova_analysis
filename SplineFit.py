from supersmoother import SuperSmoother, LinearSmoother
import pyqt_fit.nonparam_regression as smooth
from pyqt_fit import npr_methods
import random
import numpy as np
import scipy.interpolate as scinterp
import peakfinding
import sys
from scipy.optimize import minimize_scalar, minimize
import matplotlib.pyplot as plt

def moving_average(series, sigma=3):
    b = gaussian(39, sigma)
    average = filters.convolve1d(series, b/b.sum())
    var = filters.convolve1d(np.power(series-average,2), b/b.sum())
    return average, var

class Optimizer(object):
    def __init__(self, mjd, mag, error, spline, guess):
        self.mjd = mjd
        self.mag = mag
        self.error = error
        self.spline = spline
        self.guess = guess

    def GOF(self, x): #Goodness of Fit Metric for determining whether spline needs to be
        if x < 0: x = 0
        #print x
        self.spline.set_smoothing_factor(x)
        if np.isnan(self.spline(self.mjd[1])):
            self.spline.set_smoothing_factor(x + 5)
            #print 'test'
        chi_sum = 0
        
        for i in xrange(len(self.mjd)):
            square = (self.mag[i] - self.spline(self.mjd[i]))**2
            if np.isnan(self.spline(self.mjd[i])):
                ##print(self.spline(self.mjd[1] + 1))
                pass
            sigma = self.error[i] ** 2
            if i > 1:
                dx2 = self.mjd[i] - self.mjd[i-1]
                dy2 = self.spline(self.mjd[i]) - self.spline(self.mjd[i-1])
                dx1 = self.mjd[i-1] - self.mjd[i-2]
                dy1 = self.spline(self.mjd[i-1]) - self.spline(self.mjd[i-2])
                
                if dx1 == 0:
                    dx1 += 0.01
                elif dx2 == 0:
                    dx2+=0.01
                elif dy1 == 0:
                    dy1 += 0.01
                elif dy2 == 0:
                    dy1 += 0.01


                dslope = (dy2/dx2 - dy1/dx1 ) * 10**(2)

                chi_sum += (square / sigma) + (np.abs(dslope)) **2
                ##print dslope, chi_sum, square, sigma
            else:
                chi_sum += (square / sigma)
                ##print chi_sum, square, sigma, self.spline(self.mjd[i])       
        
        chi_sum = chi_sum / len(self.mjd)
        #print(chi_sum)
        return chi_sum

    def optimize(self):
        x0 = [self.guess]
        res = minimize(self.GOF, x0, method='Nelder-Mead',options={'gtol': 0.01, 'maxiter': 100, 'disp': True})
        #res = minimize(self.GOF, x0, method='SLSQP', jac = False, bounds = ((0.01,None),), options={'ftol': 1, 'eps': 0.1, 'maxiter': 100}) 
        #res = minimize(self.GOF, x0, method='L-BFGS-B', jac = False, bounds = ((0,None),), options={'maxiter': 100}) 
        #print(res.x)
        #print(res.message) 
        return res.x


def NonParam(rec, toggle, band):
    splinedat = []
    filenames = np.unique(rec.name).tolist()
    random.shuffle(filenames)

    if toggle == "Single":
        filenames = [filenames[1]]
    elif toggle == "Thirty":
        filenames = filenames[0:30]

    for filename in filenames:
        print filename
        print band
        print rec.mag
        print rec.mjd
        filters = [band]
        #filters = np.unique((rec.band))
        for flter in filters:
            idx = np.where((rec.band == flter) & (rec.name == filename))
            print idx
            banddata_unsorted = rec[idx]
            order = np.argsort(banddata_unsorted.mjd)
            banddata = banddata_unsorted[order]
            if len(banddata.mjd) > 6:
                k0 = smooth.NonParamRegression(banddata.mjd, banddata.mag, method=npr_methods.SpatialAverage()) 
                k0.fit()
                plt.plot(banddata.mjd, k0(banddata.mjd), label="Spatial Averaging", linewidth=2)
                plt.scatter(banddata.mjd, banddata.mag)
                plt.show()
    return [1,2,3,4]

def Supersmoother(rec, toggle, band):
    splinedat = []
    filenames = np.unique(rec.name).tolist()
    random.shuffle(filenames)

    if toggle == "Single":
        filenames = [filenames[1]]
    elif toggle == "Thirty":
        filenames = filenames[0:30]

    for filename in filenames:
        print filename
        print band
        print rec.mag
        print rec.mjd
        filters = [band]
        #filters = np.unique((rec.band))
        for flter in filters:
            idx = np.where((rec.band == flter) & (rec.name == filename))
            print idx
            banddata_unsorted = rec[idx]
            order = np.argsort(banddata_unsorted.mjd)
            banddata = banddata_unsorted[order]
            if len(banddata.mjd) > 6:
                for i in xrange(banddata.mjd.size - 1):
                    if banddata.mjd[i] == banddata.mjd[i+1]:
                        print("ERROR: mjd values were equal")
                        
                    if banddata.magerr[i] == 0:
                        print("ERROR: magerr = 0")
                w = 1./(banddata.magerr) ** 2 
                stype = banddata.stype[1]
                try:
                    model = SuperSmoother(alpha = 8)
                    model.fit(banddata.mjd, banddata.mag, w)
                    
                    mjd_fit = np.linspace(banddata.mjd[0], banddata.mjd[-1], 1000)
                    mag_fit = model.predict(mjd_fit)
                    
                    print "Peak to Peak 1%", np.ptp(mag_fit) * 0.01
                    maxp, minp = peakfinding.peakdetect(mag_fit, mjd_fit, 5, np.ptp(mag_fit) * 0.1)
                    minp, maxp = np.array(minp), np.array(maxp)
                except ValueError:
                    break 
                
                if len(minp) > 0 and minp[0][0] < banddata.mjd[0] + 40:
                    mjd_new = mjd_fit# - minp[0][0]
                    banddata.mjd = banddata.mjd# - minp[0][0]
            
                    mag_new = mag_fit# - minp[0][1]
                    banddata.mag = banddata.mag# - minp[0][1]
                    

                    if mjd_new[0] < 0-5 and mjd_new[-1] > 35:
                        mjd_sampled = np.linspace(-5, 35, num = 40)
                        mag_sampled = model.predict(mjd_sampled + minp[0][0]) - minp[0][1] 

                        #if all(i <= 5 for i in mag_new) and all(i >= -0.1 for i in mag_new):
                        splinedat.append({'min': minp.tolist(), 'max': maxp.tolist(),'id': filename, 'stype': stype, 'band': flter, 'splinedata': mag_new.tolist(), 'phase': mjd_new.tolist(), 'xraw': banddata.mjd.tolist(), 'yraw': banddata.mag.tolist(), 'spldata_sampled': mag_sampled.tolist(), 'mjddata_sampled': mjd_sampled.tolist(), 'magerr': banddata.magerr.tolist()})
                    else:
                        splinedat.append({'min': minp.tolist(), 'max': maxp.tolist(),'id': filename, 'stype': stype, 'band': flter, 'splinedata': mag_new.tolist(), 'phase': mjd_new.tolist(), 'xraw': banddata.mjd.tolist(), 'yraw': banddata.mag.tolist(), 'spldata_sampled': [], 'mjddata_sampled': [], 'magerr': banddata.magerr.tolist()})
#                        print(banddata.mjd.tolist(), banddata.mag.tolist())
                else:
                    splinedat.append({'mjddata_sampled': [], 'spldata_sampled': [],'min': minp.tolist(), 'max': maxp.tolist(),'id': filename, 'stype': banddata.stype.tolist(), 'band': flter, 'splinedata': mag_fit.tolist(), 'phase': mjd_fit.tolist(),'magerr': banddata.magerr.tolist(), 'xraw': banddata.mjd.tolist(), 'yraw': banddata.mag.tolist()})
            else:
                print "Insufficient Data"
    
    
    return splinedat, len(splinedat)
 
def Usplinefit(rec, toggle, band):
    splinedat = []
    filenames = np.unique(rec.name).tolist()
    random.shuffle(filenames)

    if toggle == "Single":
        filenames = [filenames[1]]
    elif toggle == "Thirty":
        filenames = filenames[0:30]

    for filename in filenames:
        print filename
        print band
        print rec.mag
        print rec.mjd
        #filters = [band]
        filters = np.unique((rec.band))
        for flter in filters:
            idx = np.where((rec.band == flter) & (rec.name == filename))
            print idx
            banddata_unsorted = rec[idx]
            order = np.argsort(banddata_unsorted.mjd)
            banddata = banddata_unsorted[order]
            if len(banddata.mjd) > 6:
                #_, var = moving_average()
                #print filename
                w = 1./(banddata.magerr) ** 2
                spl = scinterp.UnivariateSpline(banddata.mjd, banddata.mag, k = 1, w = w)
                #print 'This is the spline data originally: ', (spl(banddata.mjd[1]))
                #spl.set_smoothing_factor(1)
                #print 'This is the spline data after fixing smoothing param: ', spl.get_knots()
                #print 'This is the spline data after fixing smoothing param: ', spl.get_knots()
                
                #opt = Optimizer(banddata.mjd, banddata.mag, banddata.magerr,  spl, len(w))                
        
                #smoothing_num = opt.optimize()
                #if smoothing_num < 0: smoothing_num = 0.35
                #spl.set_smoothing_factor(smoothing_num)               
                spl.set_smoothing_factor(0.3)               
            
                #print smoothing_num

                mjd_new = np.linspace(banddata.mjd[0], banddata.mjd[-1], num = 200)
                mag_new = spl(mjd_new)
                print mag_new
                print "Peak to Peak 10% ", np.ptp(mag_new) * 0.01
                try:
                    maxp, minp = peakfinding.peakdetect(mag_new, mjd_new, 5, np.ptp(mag_new)*0.1)
                except:
                    maxp, minp = np.array([]), np.array([])
                minp = np.array(minp)
                maxp = np.array(maxp)
                print "minima: ", minp
                print "maxima: ", maxp
                
                if len(minp) > 0 and minp[0][0] < banddata.mjd[0] + 40:
                    
                    mjd_new = mjd_new - minp[0][0]
                    banddata.mjd = banddata.mjd - minp[0][0]

                    mag_new = mag_new - minp[0][1]
                    banddata.mag = banddata.mag - minp[0][1]
                    
                    stype = banddata.stype[1]
    
                    if mjd_new[0] < 0-5 and mjd_new[-1] > 35:
                        mjd_sampled = np.linspace(-5, 35, num = 40)
                        mag_sampled = spl(mjd_sampled + minp[0][0]) - minp[0][1] 

                        if all(i <= 5 for i in mag_new) and all(i >= -0.1 for i in mag_new):
                            splinedat.append({'min': minp.tolist(), 'max': maxp.tolist(),'id': filename, 'stype': stype, 'band': flter, 'splinedata': mag_new.tolist(), 'phase': mjd_new.tolist(), 'xraw': banddata.mjd.tolist(), 'yraw': banddata.mag.tolist(), 'spldata_sampled': mag_sampled.tolist(), 'mjddata_sampled': mjd_sampled.tolist(), 'magerr': banddata.magerr.tolist()})
#                    else:
#                        splinedat.append({'id': filename, 'stype': stype, 'band': flter, 'splinedata': mag_new.tolist(), 'phase': mjd_new.tolist(), 'xraw': banddata.mjd.tolist(), 'yraw': banddata.mag.tolist()})
#                        print(banddata.mjd.tolist(), banddata.mag.tolist())
                else:
                    splinedat.append({'mjddata_sampled': [], 'spldata_sampled': [],'min': minp.tolist(), 'max': maxp.tolist(),'id': filename, 'stype': banddata.stype.tolist(), 'band': flter, 'splinedata': mag_new.tolist(), 'phase': mjd_new.tolist(),'magerr': banddata.magerr.tolist(), 'xraw': banddata.mjd.tolist(), 'yraw': banddata.mag.tolist()})
            else:
                print "Insufficient Data"
    
    
    return splinedat, len(splinedat)
                  


def splinefit(rec, toggle, band):
    splinedat = []
    filenames = np.unique(rec.name).tolist()
    filenames_tmp = np.unique(rec.name).tolist()
    random.shuffle(filenames_tmp)
    
    for filename in filenames:
        filters = np.unique
        for flter in filters:
            idx = np.where((rec.band == flter) & (rec.name == filename))
            banddata_unsorted = rec[idx]
            if len(banddata_unsorted.mjd) > 6:
                order = np.argsort(banddata_unsorted.mjd)
                banddata = banddata_unsorted[order]
                mjd_sampled_ind = np.arange(2, find_nearest_ind(banddata.mjd, banddata.mjd.min() + 25), 4)
                sparse =  np.arange(find_nearest_ind(banddata.mjd, banddata.mjd.min() + 25), find_nearest_ind(banddata.mjd, banddata.mjd.max()), 10)
                idx_final = np.append(mjd_sampled_ind, sparse)
                mjd_sampled = banddata.mjd[idx_final]
                
                mjd_new = np.linspace(banddata.mjd.min(), banddata.mjd.max(), num = 200)
                spl1d = scinterp.interp1d(banddata.mjd, banddata.mag)
                maxp, minp = peakfinding.peakdetect(spl1d(mjd_new), mjd_new, 10, 0.03)
                
                minp = np.array(minp)
                maxp = np.array(maxp)
                mag_knot = []
                minp3 = []
                maxp3 = []

                if len(minp) > 0 and minp[0][0] < (banddata.mjd.min() + 25) and minp[0][0] > banddata.mjd.min():
                    
                                            
                    try: 
                        tck = scinterp.splrep(banddata.mjd, banddata.mag, t = mjd_sampled, w = 1./(banddata.magerr)**2)
                    except:
                        #print mjd_sampled
                        pass
                    mag_knot = scinterp.splev(mjd_new, tck)
                    maxp3, minp3 = peakfinding.peakdetect(mag_knot, mjd_new, 20, 0.1)
                    
                    mjd_20 = np.linspace(minp[0][0] - 5, minp[0][0] + 20, num = 30)
                    splinedata = scinterp.splev(mjd_20, tck)

                    #phase correction
                        
                    mjd_20 = mjd_20 - minp[0][0]
                        
                    #magnitude correction
                    splinedata = splinedata - banddata.mag.min()
                                    
                    banddata.stype = banddata.stype[1]                    

                    splinedat.append({'id': filename, 'dataset': 2, 'band': flter, 'splinedata': splinedata.tolist(), 'phase': mjd_20.tolist()})
    return splinedat, len(splinedat)
 
if __name__ == '__main__':
    sys.exit()



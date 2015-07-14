import random
import numpy as np
import scipy.interpolate as scinterp
import peakfinding
import sys


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
                    
                                            
                    print flter
                    try: 
                        tck = scinterp.splrep(banddata.mjd, banddata.mag, t = mjd_sampled, w = 1./(banddata.magerr)**2)
                    except:
                        print mjd_sampled
                    mag_knot = scinterp.splev(mjd_new, tck)
                    maxp3, minp3 = peakfinding.peakdetect(mag_knot, mjd_new, 20, 0.1)
                    
                    mjd_20 = np.linspace(minp[0][0] - 5, minp[0][0] + 20, num = 30)
                    splinedata = scinterp.splev(mjd_20, tck)

                    #phase correction
                        
                    mjd_20 = mjd_20 - minp[0][0]
                        
                    #magnitude correction
                    splinedata = splinedata - banddata.mag.min()
                                    
                    splinedat.append({'id': filename, 'dataset': 2, 'band': flter, 'splinedata': splinedata.tolist(), 'phase': mjd_20.tolist()})
    return splinedat

def Usplinefit(rec, toggle, band):
    splinedat = []
    filenames = np.unique(rec.name).tolist()
    random.shuffle(filenames)

    if toggle == "Single":
        filenames = [filenames[1]]

    for filename in filenames:
        filters = [band]
        #filters = np.unique((rec.band))
        for flter in filters:
            idx = np.where((rec.band == flter) & (rec.name == filename))
            banddata_unsorted = rec[idx]
            order = np.argsort(banddata_unsorted.mjd)
            banddata = banddata_unsorted[order]
                        
            if len(banddata.mjd) > 6:
                print 'test'
                spl = scinterp.UnivariateSpline(banddata.mjd, banddata.mag, k = 1)
                spl.set_smoothing_factor(0.35)
                mjd_new = np.linspace(banddata.mjd[0], banddata.mjd[-1], num = 200)
                mag_new = spl(mjd_new)
                maxp, minp = peakfinding.peakdetect(mag_new, mjd_new, 5, 0.03)
                
                minp = np.array(minp)
                maxp = np.array(maxp)
                print minp
                
                if len(minp) > 0 and minp[0][0] < 10 and minp[0][0] > -5:
                    
                    mjd_new = mjd_new - minp[0][0]
                    banddata.mjd = banddata.mjd - minp[0][0]

                    mag_new = mag_new - minp[0][1]
                    banddata.mag = banddata.mag - minp[0][1]
                    
                    #if all(i <= 5 for i in mag_new) and all(i >= -5 for i in mag_new):
                    splinedat.append({'id': filename, 'dataset': 1, 'band': flter, 'splinedata': mag_new.tolist(), 'phase': mjd_new.tolist(), 'xraw': banddata.mjd, 'yraw': banddata.mag})
                else:
                    splinedat.append({'id': filename, 'dataset': 1, 'band': flter, 'splinedata': [], 'phase': [], 'xraw': banddata.mjd, 'yraw': banddata.mag})
    
    return splinedat
               
if __name__ == '__main__':
    sys.exit()


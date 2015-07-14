import itertools
import numpy as np
from LightcurveClass import Lightcurve
import sys
import os
        

def readin_aavso(filename):
    formatcode = ('f8,'*4 + '|S16,'*20).rstrip(',')
    data = np.recfromtxt(filename, delimiter='\t', names=True, dtype=formatcode,autostrip=True,case_sensitive='lower', invalid_raise=False)

    ind = np.where((data.band == 'V') & (data.uncertainty > 0) & (np.isnan(data.uncertainty) == 0) & (data.uncertainty < 0.02))
    banddata = data[ind]
    return banddata

def hstack2(arrays):
    return arrays[0].__array_wrap__(np.hstack(arrays))

def readin_SNANA(filename):
    #data = 
    path = '/Users/zaidi/Documents/REU/SNDATA/lcmerge/'
    formatcode = ('|S16,'.rstrip(':') + 'f8,'+ '|S16,'*2 + 'f8,'*4 )
    data = np.recfromtxt(os.path.join(path,filename),dtype = formatcode, names = True, skip_header = 19, case_sensitive='lower', invalid_raise = False)
    #header = np.recfromtxt(filename, 
    return data


def SNrest():
    path = "./data/restframe/"
    objnames, band, mjd, mag, magerr = [],[],[],[],[]
    formatcode = ('|S16,'.rstrip('#') +'f8,'*6 + '|S16,' + 4 * 'f8,' + '|S16,' * 3 + 'f8,' * 2 + '|S16,' + 'f8,' * 2)
    filenames = os.listdir("./data/restframe/")
    for filename in filenames:
        data = np.recfromtxt(os.path.join(path, filename),usecols = (0,1,2,3,4), dtype = formatcode, names = True, skip_header = 13, case_sensitive = 'lower', invalid_raise = False)
        name = np.empty(len(data.band), dtype = 'S20')
        name.fill(filename)
        objnames.append(name)
        band.append(data.band)
        mjd.append(data.phase)
        mag.append(data.mag)
        magerr.append(data.err)
        
    objnames = np.fromiter(itertools.chain.from_iterable(objnames), dtype = 'S20')
    band = np.fromiter(itertools.chain.from_iterable(band), dtype = 'S16')
    mjd = np.fromiter(itertools.chain.from_iterable(mjd), dtype = 'float')
    mag = np.fromiter(itertools.chain.from_iterable(mag), dtype = 'float')
    magerr = np.fromiter(itertools.chain.from_iterable(magerr), dtype = 'float')
    LC = Lightcurve(objnames, band, mjd, mag, magerr)
    return LC


def harvard():
    path = './data/lc.standardsystem.sesn_allphot.dat'
    formatcode = ('|S16,' + '|S16,' + 'f8,' * 3 + '|S16,')
    data = np.recfromtxt(path, dtype = formatcode, names = ['name', 'band', 'mjd', 'mag', 'magerr', 'survey'], case_sensitive = 'lower', invalid_raise = False)
    data.band = np.array([x.replace('prime','',1) for x in data.band.tolist()])
    
    LC = Lightcurve(data.name, data.band, data.mjd, data.mag, data.magerr)
    return LC




if __name__=='__main__':
    sys.exit()

import itertools
import numpy as np
from LightcurveClass import Lightcurve
import sys
import os
import re
import cPickle as pickle
        
'''
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        if input object is a ndarray it will be converted into a dict holding dtype, shape and the data base64 encoded
        """
        if isinstance(obj, np.ndarray):
            data_b64 = base64.b64encode(obj.data)
            return dict(__ndarray__=data_b64,
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder(self, obj)

def json_numpy_obj_hook(dct):
    """
    Decodes a previously encoded numpy ndarray
    with proper shape and dtype
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct
'''



def readin_aavso(filename):
    formatcode = ('f8,'*4 + '|S16,'*20).rstrip(',')
    data = np.recfromtxt(filename, delimiter='\t', names=True, dtype=formatcode,autostrip=True,case_sensitive='lower', invalid_raise=False)

    ind = np.where((data.band == 'V') & (data.uncertainty > 0) & (np.isnan(data.uncertainty) == 0) & (data.uncertainty < 0.02))
    banddata = data[ind]
    return banddata

def hstack2(arrays):
    return arrays[0].__array_wrap__(np.hstack(arrays))

def SNANA(filename):
    path = './data/lcmerge/'
    formatcode = ('|S16,'.rstrip(':') + 'f8,'+ '|S16,'*2 + 'f8,'*4 )
    data = np.recfromtxt(os.path.join(path,filename),dtype = formatcode, names = True, skip_header = 19, case_sensitive='lower', invalid_raise = False)
    #header = np.recfromtxt(filename, 
    return data


def SNrest():
    path = "./data/restframe/"
    objnames, band, mjd, mag, magerr, stype = [],[],[],[],[], []
    formatcode = ('|S16,'.rstrip('#') +'f8,'*6 + '|S16,' + 4 * 'f8,' + '|S16,' * 3 + 'f8,' * 2 + '|S16,' + 'f8,' * 2)
    filenames = os.listdir(path)
    for filename in filenames:
        data = np.recfromtxt(os.path.join(path, filename),usecols = (0,1,2,3,4), dtype = formatcode, names = True, skip_header = 13, case_sensitive = 'lower', invalid_raise = False)
        name = np.empty(len(data.band), dtype = 'S20')
        name.fill(filename)
        objnames.append(name)
        data.band = [x.lower() for x in data.band]
        band.append(data.band)
        mjd.append(data.phase)
        mag.append(data.mag)
        magerr.append(data.err)
        
        
    objnames = np.fromiter(itertools.chain.from_iterable(objnames), dtype = 'S20')
    band = np.fromiter(itertools.chain.from_iterable(band), dtype = 'S16')
    mjd = np.fromiter(itertools.chain.from_iterable(mjd), dtype = 'float')
    mag = np.fromiter(itertools.chain.from_iterable(mag), dtype = 'float')
    magerr = np.fromiter(itertools.chain.from_iterable(magerr), dtype = 'float')
    stype = np.full(len(objnames), 1)
    LC = Lightcurve(objnames, band, mjd, mag, magerr, stype)
    return LC


def harvard():
    path = './data/lc.standardsystem.sesn_allphot.dat'
    formatcode = ('|S16,' + '|S16,' + 'f8,' * 3 + '|S16,')
    data = np.recfromtxt(path, dtype = formatcode, names = ['name', 'band', 'mjd', 'mag', 'magerr', 'survey'], case_sensitive = 'lower', invalid_raise = False)
    data.band = np.array([x.lower() for x in data.band])
    stype = np.full(len(data.name), 2)
    LC = Lightcurve(data.name, data.band, data.mjd, data.mag, data.magerr, stype)
    return LC


def DESplusHOSTZ():

    try:
        DESplusHOSTZ = pickle.load( open( "DESplusHOSTZ_pdump", "rb"))
        print DESplusHOSTZ.toRecArray()
        return DESplusHOSTZ
    except:

        lookup = 'NVAR'
        objnames, band, mjd, mag, magerr = [],[],[],[],[] 
        path = './data/DES_BLIND+HOSTZ/'
        filenames = os.listdir(path)
                
        linenum = 16
        
        #initialize data structure to store the data
        

        lookup = [3730,4490,4760,4810]
        for filename in filenames:
            if filename.endswith('.DAT'):
                data = np.recfromtxt(os.path.join(path, filename), usecols = (1,2,4,5), names = ['mjd', 'band', 'mag', 'err'], skip_header = 19, skip_footer = 1, case_sensitive = 'lower', invalid_raise = False)
                name = np.empty(len(data.band), dtype = 'S20')
                name.fill(filename)
                '''
                #convert flux to magnitude
                for i, flt in enumerate(data.band):
                    if flt == 'g':
                        print data.mag[i], ' ',
                        print data.err[i]
                        data.mag[i] = np.log10(data.mag[i] / 3730.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 3730.) * -2.5
                    if flt == 'r':
                        data.mag[i] = np.log10(data.mag[i] / 4490.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 4490.) * -2.5
                    if flt == 'i':
                        data.mag[i] = np.log10(data.mag[i] / 4760.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 4760.) * -2.5
                    if flt == 'z':
                        data.mag[i] = np.log10(data.mag[i] / 4810.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 4810.) * -2.5
                '''
                objnames.append(name)
                band.append(data.band)
                mjd.append(data.mjd)
                 
                mag.append(data.mag)
                magerr.append(data.err)
         
        objnames = np.fromiter(itertools.chain.from_iterable(objnames), dtype = 'S20')
        band = np.fromiter(itertools.chain.from_iterable(band), dtype = 'S16')
        mjd = np.fromiter(itertools.chain.from_iterable(mjd), dtype = 'float')
        mag = np.fromiter(itertools.chain.from_iterable(mag), dtype = 'float')
        magerr = np.fromiter(itertools.chain.from_iterable(magerr), dtype = 'float')
        stype = np.full(len(objnames), 1)
        LC = Lightcurve(objnames, band, mjd, mag, magerr, stype)
        pickle.dump( LC, open("DESplusHOSTZ_pdump", "wb"))
        DESplusHOSTZ()

def DESnoHOSTZ():

    try:
        DESnoHOSTZ = pickle.load( open( "DESnoHOSTZ_pdump", "rb"))
        print DESnoHOSTZ.toRecArray()
        return DESnoHOSTZ
    except:

        lookup = 'NVAR'
        objnames, band, mjd, mag, magerr,stype = [],[],[],[],[],[] 
        path = './data/DES_BLINDnoHOSTZ/'
        filenames = os.listdir(path)
                
        linenum = 16
        
        #initialize data structure to store the data
        
        stype_txt = np.recfromtxt('./data/TEST+HOST.KEY', usecols = (1,2,3,4,5,6), names = ['cid', 'gentype', 'sntype', 'genz', 'hostz', 'hostzerr'], skip_header = 2, case_sensitive = 'lower', invalid_raise = False)

        lookup = [3730,4490,4760,4810]
        for filename in filenames:
            if filename.endswith('.DAT'):
                data = np.recfromtxt(os.path.join(path, filename), usecols = (1,2,4,5), names = ['mjd', 'band', 'mag', 'err'], skip_header = 19, skip_footer = 1, case_sensitive = 'lower', invalid_raise = False)
                name = np.zeros(len(data.band), dtype = 'S20')
                sntype = np.zeros(len(data.band), dtype = '=i4')
                idx = np.where(stype_txt.cid == filename[6:-4].lstrip('0'))#get rid of fluff around filename to get cid
                if len(idx[0]) != 0:
                    sntype_tmp = np.asscalar(stype_txt.gentype[idx])
                    sntype_tmp = int(sntype_tmp)
                else:
                    sntype_tmp = -9
                    
                name.fill(filename)
                sntype.fill(sntype_tmp)
                '''
                #convert flux to magnitude
                for i, flt in enumerate(data.band):
                    if flt == 'g':
                        print data.mag[i], ' ',
                        print data.err[i]
                        data.mag[i] = np.log10(data.mag[i] / 3730.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 3730.) * -2.5
                    if flt == 'r':
                        data.mag[i] = np.log10(data.mag[i] / 4490.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 4490.) * -2.5
                    if flt == 'i':
                        data.mag[i] = np.log10(data.mag[i] / 4760.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 4760.) * -2.5
                    if flt == 'z':
                        data.mag[i] = np.log10(data.mag[i] / 4810.) * -2.5
                        data.err[i] = np.log10(data.err[i] / 4810.) * -2.5
                '''
                objnames.append(name)
                band.append(data.band)
                mjd.append(data.mjd)
                stype.append(sntype)
                mag.append(data.mag)
                magerr.append(data.err)
         
        objnames = np.fromiter(itertools.chain.from_iterable(objnames), dtype = 'S20')
        stype = np.fromiter(itertools.chain.from_iterable(stype), dtype = 'S20')
        band = np.fromiter(itertools.chain.from_iterable(band), dtype = 'S16')
        mjd = np.fromiter(itertools.chain.from_iterable(mjd), dtype = 'float')
        mag = np.fromiter(itertools.chain.from_iterable(mag), dtype = 'float')
        magerr = np.fromiter(itertools.chain.from_iterable(magerr), dtype = 'float')

        
            
        print set(stype)
        setofsn = list(set(stype))
        for i in range(len(setofsn)):
            idx = np.where(stype == setofsn[i])
            print 'Type {} has length'.format(i), len(stype[idx])
        LC = Lightcurve(objnames, band, mjd, mag, magerr, stype)
       
        print stype[1000], ' ', objnames[1000], band[1000]
        pickle.dump( LC, open("DESnoHOSTZ_pdump", "wb"))
        DESnoHOSTZ()
        


if __name__=='__main__':
    
    DESnoHOSTZ()
    sys.exit()

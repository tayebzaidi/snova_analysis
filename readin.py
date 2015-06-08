import numpy as np
import sys
import os

def readin_aavso(filename):
    formatcode = ('f8,'*4 + '|S16,'*20).rstrip(',')
    data = np.recfromtxt(filename, delimiter='\t', names=True, dtype=formatcode,autostrip=True,case_sensitive='lower', invalid_raise=False)

    ind = np.where((data.band == 'V') & (data.uncertainty > 0) & (np.isnan(data.uncertainty) == 0) & (data.uncertainty < 0.02))
    banddata = data[ind]
    return banddata


def readin_SNANA(filename):
    #data = 
    #for filename in filenames:
    formatcode = ('|S16,'.rstrip(':') + 'f8,'+ '|S16,'*2 + 'f8,'*4 )
    data = np.recfromtxt(filename,dtype = formatcode, names = True, skip_header = 15, case_sensitive='lower', invalid_raise = False)
    dat = {}
    header = {}
    return data, header

def readin_SNrest(filename):
    path = "/Users/zaidi/Documents/REU/restframe/"
    #for filename in os.listdir(path):
    current_file = os.path.join(path, filename)
    formatcode = ('|S16,'.rstrip('#') +'f8,'*6 + '|S16,' + 4 * 'f8,' + '|S16,' * 3 + 'f8,' * 2 + '|S16,' + 'f8,' * 2)
    data = np.recfromtxt(current_file,usecols = (0,1,2,3,4,5,6), dtype = formatcode, names = True, skip_header = 13, case_sensitive = 'lower', invalid_raise = False)
    ind = np.where((data.band == 'V'))
    banddata = data[ind]
    return banddata

if __name__=='__main__':
    sys.exit()

#!/usr/bin/env/ python
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

def find_nearest_ind(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def readin_SNrest(filename):
    path = "/Users/zaidi/Documents/REU/restframe/"
    formatcode = ('|S16,'.rstrip('#') +'f8,'*6 + '|S16,' + 4 * 'f8,' + '|S16,' * 3 + 'f8,' * 2 + '|S16,' + 'f8,' * 2)
    data = np.recfromtxt(os.path.join(path, filename),usecols = (0,1,2,3,4), dtype = formatcode, names = True, skip_header = 13, case_sensitive = 'lower',             invalid_raise = False)
    return data

def readin_lcstandard_harvard():
    path = '/Users/zaidi/Downloads/lc.standardsystem.sesn_allphot.dat'
    formatcode = ('|S16,' + '|S16,' + 'f8,' * 3 + '|S16,')
    data = np.recfromtxt(path, dtype = formatcode, names = ['filename', 'flt', 'mjd', 'mag', 'magerr', 'survey'], case_sensitive = 'lower', invalid_raise = False)
    data.flt = np.array([x.replace('prime','',1) for x in data.flt.tolist()])
    return data

def main()
    data = readin

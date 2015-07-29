#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import random
import os

def nearest_idx(array, value):
    idx = np.abs(array - value).argmin()

def main():
    splinedat = [{}] #initialize splinedata (array of dictionaries for future JSON conversion)
    dirname = os.path.dirname(os.path.abspath(__file__))
    filenames = readin.filenames_all() #use the readin module to get a list of all relevant filenames
    for filename in filenames:
        print filename
        data = readin.readin_all(filename) #use the readin module to get the relevant recarray
        filters = list(set(data.band)) #make a set containing one of each filter present
        for flter in filters:
            idx = np.where(data.band == flter)
            banddata = data[idx]
            
            if len(banddata.mjd) > 10:
                order = np.argsort(banddata.mjd)
                banddata = banddata[order]
                # reorder the data so date is monotonically increasing
                
                mjd_sampled_idx = np.arange(2, nearest_ind(banddata.mjd, banddata.mjd.min() + 25), 7
                
        

if __name__ == '__main__':
    main()

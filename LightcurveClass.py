import numpy as np
import sys
import os

def hstack2(arrays) :
  return arrays[0].__array_wrap__(np.hstack(arrays))

class Lightcurve(object):
    def __init__(self, name, band, mjd, mag, magerr):
        self.name = name
        self.band = band
        self.mjd = mjd
        self.mag = mag
        self.magerr = magerr

    def toRecArray(self):
        self.rec = np.recarray((len(self.name),),dtype=[('name', 'S20'), ('band', 'S20'), ('mjd', float), ('mag', float), ('magerr', float)])
        self.rec.name = self.name
        self.rec.band = self.band
        self.rec.mjd = self.mjd
        self.rec.mag = self.mag
        self.rec.magerr = self.magerr
        return self.rec

def combine2(LC1, LC2):
    stacked = hstack2((LC1, LC2))
    return stacked 

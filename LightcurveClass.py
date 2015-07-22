import numpy as np
import sys
import os

def hstack2(arrays) :
  return arrays[0].__array_wrap__(np.hstack(arrays))

class Lightcurve(object):
    def __init__(self, name, band, mjd, mag, magerr, stype):
        self.name = name
        self.band = band
        self.mjd = mjd
        self.mag = mag
        self.magerr = magerr
        self.stype = stype

    def toRecArray(self):
        self.rec = np.recarray((len(self.name),),dtype=[('name', 'S20'), ('band', 'S20'), ('mjd', float), ('mag', float), ('magerr', float), ('stype', int)])
        self.rec.name = self.name
        self.rec.band = self.band
        self.rec.mjd = self.mjd
        self.rec.mag = self.mag
        self.rec.magerr = self.magerr
        self.rec.stype = self.stype
        return self.rec

def combine2(LC1, LC2):
    stacked = hstack2((LC1, LC2))
    return stacked 

import numpy as np
import sys
import os

class Lightcurve(object):
    def __init__(self, name, band, mjd, mag, magerr):
        self.name = name
        self.band = band
        self.mjd = mjd
        self.mag = mag
        self.magerr = magerr

    def toRecArray(self):
        rec = np.recarray((len(self.name),),dtype=[('name', 'S20'), ('band', 'S20'), ('mjd', float), ('mag', float), ('magerr', float)])
        rec.name = self.name
        rec.band = self.band
        rec.mjd = self.mjd
        rec.mag = self.mag
        rec.magerr = self.magerr
        return rec

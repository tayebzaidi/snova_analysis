#!/usr/bin/env python
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backend_bases import key_press_handler
from LightcurveClass import Lightcurve
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure
import sys
import peakfinding
import scipy.interpolate as scinterp
import itertools
import random
import os

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def find_nearest_ind(array,value):
    idx = np.abs(array-value).argmin()
    return idx

def readin_SNrest():
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


def readin_lcstandard_harvard():
    path = '.data/lc.standardsystem.sesn_allphot.dat'
    formatcode = ('|S16,' + '|S16,' + 'f8,' * 3 + '|S16,')
    data = np.recfromtxt(path, dtype = formatcode, names = ['filename', 'flt', 'mjd', 'mag', 'magerr', 'survey'], case_sensitive = 'lower', invalid_raise = False)
    data.flt = np.array([x.replace('prime','',1) for x in data.flt.tolist()])
    
    return data

class LCVisualization(Tk.Frame):
    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI(parent)
        

    def initUI(self, parent):
        
        self.parent.title("LC Visualization")
    
        self.menu = Tk.Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Beep", command=self.bell())
        self.menu.add_command(label="Exit", command=self.onExit)
    
        self.parent.bind("<Double-Button-1>", self.showMenu)
        self.grid(row=0,padx=5,pady=5)    
       
        self.ButtonFrame=Tk.Frame(bd=1, relief=Tk.SUNKEN)
        self.ButtonFrame.grid(row=0,padx=5,pady=5, column=0)        

        #initialize variables here
        self.dataHV = Tk.StringVar()
        self.dataRFrame = Tk.StringVar()
        self.band = Tk.StringVar()
        self.toggle = Tk.StringVar()
        self.rec = self.GetData()

        self.initFigure(parent)
        self.DataSelect(parent)
        self.BandRadioButtons()
        self.Selection()


        # This is where I begin the matplotlib code first initializing the Figure 

    def initFigure(self, parent):
        self.f = matplotlib.figure.Figure(figsize=(9,9), dpi=90)
        self.ax0 = self.f.add_subplot(1,1,1)
        #self.ax0.set_aspect(1)

        self.ax0.set_xlabel( 'Time (days)' )
        self.ax0.set_ylabel( 'Magnitude (Inverted)' )

        self.frame = Tk.Frame(parent)
        self.frame.grid(row=0,padx=5,pady=5, column = 1)
 
        self.canvas = tkagg.FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0,padx=5,pady=5)
        self.canvas.show()
     
        self.toolbar = tkagg.NavigationToolbar2TkAgg(self.canvas, self.frame )
        self.toolbar.grid(row=2)
        self.toolbar.update()

    # Create method Plot to allow for on the fly adjustment of the plotting
    def Plot(self):
        self.ax0.clear()
        splinedat = splinefit(self.rec, self.toggle.get(), self.band.get())
        
        for data in splinedat:
                ydata = data['splinedata']
                xdata = data['phase'] 
                self.ax0.plot(xdata, ydata)

        self.canvas.show()
        
            

        #self.ax0.plot([3,2,1])
        #    self.canvas.show()

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.quit()

    def GetData(self):
        LC = readin_SNrest() 
        rec = LC.toRecArray()
        return rec


    #Define Checkboxes for the Data Selection
    def DataSelect(self, parent):
        self.DataFrame = Tk.Frame(bd=1, relief=Tk.SUNKEN, master = self.ButtonFrame)
        self.DataFrame.grid(row=0,padx=5,pady=5)
        Tk.Checkbutton(self.DataFrame, text="HarvardLC", variable = self.dataHV, command = self.datacheck).grid(row=0,padx=5,pady=5) 
        Tk.Checkbutton(self.DataFrame, text="Restframe", variable = self.dataRFrame, command = self.datacheck).grid(row=1)

    def Selection(self):
        self.ToggleFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN, master = self.ButtonFrame)
        self.ToggleFrame.grid(row=1)
        self.toggle.set('Single')
        Tk.Radiobutton(self.ToggleFrame, text="Single", variable = self.toggle,value = "Single", command=self.togglecheck).grid(row=0,padx=5,pady=5)
        Tk.Radiobutton(self.ToggleFrame, text="All", variable=self.toggle, value = "All", command = self.togglecheck).grid(row=1,padx=5,pady=5)

    def BandRadioButtons(self):
        self.RBFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN, master = self.ButtonFrame)
        self.RBFrame.grid(row=2,padx=5,pady=5)
        Buttons = set(self.rec.band)  #Define the Buttons to be a set of all possible bands
        for i,text in enumerate(Buttons):
            Tk.Radiobutton(self.RBFrame, text='Band %s' % text, variable = self.band, value = text,command = self.bandcheck).grid(row=i)

    def SplineFitType(self):
        pass

 
    #Define the commands all the Buttons are tied to
    
    #Start with the Data Selection commands
    def datacheck(self):
        print self.dataHV.get(), " ", self.dataRFrame.get()

    def bandcheck(self):
        print self.band.get()

    def togglecheck(self):
        print self.toggle.get()
        self.Plot()

def splinefit(rec, toggle, band):
    splinedat = []
    if toggle == "All":
        filenames = np.unique(rec.name).tolist()
    else:
        filenames_tmp = np.unique(rec.name).tolist()
        random.shuffle(filenames_tmp)
        filenames = [filenames_tmp[1]]
    for filename in filenames:
        filters = [band]
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
    print splinedat
    return splinedat



    

def main():
    root = Tk.Tk()
    #root.geometry("500x1000+300+300")
    app = LCVisualization(root)
    root.update()
    root.deiconify()
    root.mainloop()



if __name__ == '__main__':
   main() 

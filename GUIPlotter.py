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
import SplineFit
import readin

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
        self.stype = Tk.StringVar()
        self.rec = self.GetData()

        self.initFigure(parent)
        self.DataSelect(parent)
        self.BandRadioButtons()
        self.SplineFitType()
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

        self.canvas.mpl_connect('pick_event', self.onPick)         

    # Create method Plot to allow for on the fly adjustment of the plotting
    def Plot(self):
        self.ax0.clear()
        if self.stype.get() == "UnivariateSpline":
            splinedat = SplineFit.Usplinefit(self.rec, self.toggle.get(), self.band.get())
        else:
            splinedat = SplineFit.splinefit(self.rec, self.toggle.get(), self.band.get())
        
        for data in splinedat:
                ydata = data['splinedata']
                xdata = data['phase'] 
                if self.toggle.get() != "All":
                    xraw = data['xraw']
                    yraw = data['yraw']
                    self.ax0.scatter(xraw, yraw)
                self.ax0.plot(xdata, ydata)

        self.canvas.show()
        
            

        #self.ax0.plot([3,2,1])
        #    self.canvas.show()

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onPick(self, event):
        ind = event.ind
        print 'onpick3 scatter:', ind, npy.take(x, ind), npy.take(y, ind)

    def onExit(self):
        self.quit()

    def GetData(self):
        LCR = readin.SNrest()
        LCHV = readin.harvard()
        #LCDES = 
        rec = LCHV.toRecArray()
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
        self.band.set("B")
        Buttons = set(self.rec.band)  #Define the Buttons to be a set of all possible bands
        for i,text in enumerate(Buttons):
            text = Tk.Radiobutton(self.RBFrame, text='Band %s' % text, variable = self.band, value = text,command = self.bandcheck).grid(row=i)

    def SplineFitType(self):
        self.STypeFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN, master= self.ButtonFrame)  
        self.STypeFrame.grid(row=3, padx=5, pady=5)
        self.stype.set("UnivariateSpline")
        Tk.Radiobutton(self.STypeFrame, text="Univariate", variable = self.stype, value = "UnivariateSpline", command = self.sftype).grid(row=0,padx=5,pady=5)
        Tk.Radiobutton(self.STypeFrame, text="Splrep", variable = self.stype, value = "splrep", command = self.sftype).grid(row=1,padx=5,pady=5)
        

    #Define the commands all the Buttons are tied to
    
    #Start with the Data Selection commands
    def datacheck(self):
        print self.dataHV.get(), " ", self.dataRFrame.get()

    def bandcheck(self):
        print self.band.get()

    def togglecheck(self):
        print self.toggle.get()
        self.Plot()

    def sftype(self):
        print self.stype.get()
    

def main():
    root = Tk.Tk()
    #root.geometry("500x1000+300+300")
    app = LCVisualization(root)
    root.update()
    root.deiconify()
    root.mainloop()



if __name__ == '__main__':
   main() 

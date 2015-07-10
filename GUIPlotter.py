#!/usr/bin/env python
import itertools
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backend_bases import key_press_handler
from LightcurveClass import Lightcurve
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure
import sys
import os

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

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
    print objnames
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
        self.pack()    
       
        #initialize variables here
        self.dataHV = Tk.StringVar()
        self.dataRFrame = Tk.StringVar()
        self.band = Tk.StringVar()
        self.toggle = Tk.StringVar()

        self.initFigure(parent)
        self.DataSelect(parent)
        self.BandRadioButtons(parent)
        self.Selection(parent)

        self.GetData()

        # This is where I begin the matplotlib code first initializing the Figure 

    def initFigure(self, parent):
        self.f = matplotlib.figure.Figure(figsize=(5,5), dpi=90)
        self.ax0 = self.f.add_subplot(1,1,1)
        self.ax0.set_aspect(1)

        self.ax0.set_xlabel( 'Time (days)' )
        self.ax0.set_ylabel( 'Magnitude (Inverted)' )

        self.frame = Tk.Frame(parent)
        self.frame.pack(anchor=Tk.N, pady = 5, padx = 5)
 
        self.canvas = tkagg.FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=Tk.BOTH)
        self.canvas.show()
     
        self.toolbar = tkagg.NavigationToolbar2TkAgg(self.canvas, self.frame )
        self.toolbar.pack()
        self.toolbar.update()

    # Create method Plot to allow for on the fly adjustment of the plotting
    def Plot(self, parent):
        #if self.togglecheck == 'Single':
            #self.InitFigure(parent)
        self.ax0.plot([1,2,3])
        self.canvas.show()

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.quit()

    def GetData(self):
        LC = readin_SNrest() 
        rec = LC.toRecArray()
        print rec
        return LC


    #Define Checkboxes for the Data Selection
    def DataSelect(self, parent):
        self.DataFrame = Tk.Frame(bd=1, relief=Tk.SUNKEN)
        self.DataFrame.pack( padx = 5, pady = 5)
        Tk.Checkbutton(self.DataFrame, text="HarvardLC", variable = self.dataHV, command = self.datacheck).pack(anchor=Tk.NW) 
        Tk.Checkbutton(self.DataFrame, text="Restframe", variable = self.dataRFrame, command = self.datacheck).pack(anchor=Tk.NW)

    def Selection(self, parent):
        self.ToggleFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN)
        self.ToggleFrame.pack(padx=5, pady = 5)
        #self.toggle.set('All')
        Tk.Radiobutton(self.ToggleFrame, text="Single", variable = self.toggle,value = "Single", command=self.togglecheck(parent)).pack(anchor=Tk.NW)
        Tk.Radiobutton(self.ToggleFrame, text="All", variable=self.toggle, value = "All", command = self.togglecheck(parent)).pack(anchor=Tk.NW)
        print self.toggle.get()

    def BandRadioButtons(self, parent):
        self.RBFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN)
        self.RBFrame.pack(padx = 5, pady = 5)
        #Buttons = zip(list(set(data.band)), list(set(data.band))) 
        #for text, mode in Buttons:
        #    Tk.Radiobutton(self.RBFrame, text=text, variable = self.band, value = 'B',command = self.bandcheck).pack(anchor=Tk.NW)
            
        Tk.Radiobutton(self.RBFrame, text="B Band", variable = self.band, value = 'B',command = self.bandcheck).pack(anchor=Tk.NW)
        Tk.Radiobutton(self.RBFrame, text="V Band", variable = self.band, value = 'V',command = self.bandcheck).pack(anchor=Tk.NW) 
        Tk.Radiobutton(self.RBFrame, text="R Band", variable = self.band, value = 'R',command = self.bandcheck).pack(anchor=Tk.NW) 
        Tk.Radiobutton(self.RBFrame, text="I Band", variable = self.band, value = 'I',command = self.bandcheck).pack(anchor=Tk.NW) 
        Tk.Radiobutton(self.RBFrame, text="All", variable = self.band, value = 'All',command = self.bandcheck).pack(anchor=Tk.NW) 

    #Define the commands all the Buttons are tied to
    
    #Start with the Data Selection commands
    def datacheck(self):
        print self.dataHV.get(), " ", self.dataRFrame.get()

    def bandcheck(self):
        print self.band.get()

    def togglecheck(self, parent):
        print self.toggle.get()
        self.Plot(parent)

def main():
    root = Tk.Tk()
    root.geometry("900x900+300+300")
    app = LCVisualization(root)
    root.update()
    root.deiconify()
    root.mainloop()



if __name__ == '__main__':
   main() 

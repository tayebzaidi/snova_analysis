#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backend_bases import key_press_handler
import numpy as np

import matplotlib.figure
import sys
import os

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def readin_SNrest():
    path = "./data/restframe/"
    formatcode = ('|S16,'.rstrip('#') +'f8,'*6 + '|S16,' + 4 * 'f8,' + '|S16,' * 3 + 'f8,' * 2 + '|S16,' + 'f8,' * 2)
    filenames = os.listdir("./data/restframe/")
    data = np.recfromtxt(os.path.join(path, filename),usecols = (0,1,2,3,4), dtype = formatcode, names = True, skip_header = 13, case_sensitive = 'lower', invalid_raise = False)
    return data

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

        self.Checkboxes(parent)
        self.initFigure(parent)

        # This is where I begin the matplotlib code first initializing the Figure and 

    def initFigure(self, parent):
        self.f = matplotlib.figure.Figure(figsize=(5,5), dpi=90)
        self.ax0 = self.f.add_axes( (0.35, .25, .50, .50), axisbg=(.75,.75,.75), frameon=False)

        self.ax0.set_xlabel( 'Time (days)' )
        self.ax0.set_ylabel( 'Magnitude (Inverted)' )
        print self.var.get()
        print 'test'
        if self.var.get() == "on":
            self.ax0.plot([1,2,3])

        self.frame = Tk.Frame( parent )
        self.frame.pack()
 
        self.canvas = tkagg.FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack()
        self.canvas.show()
     
        self.toolbar = tkagg.NavigationToolbar2TkAgg(self.canvas, self.frame )
        self.toolbar.pack()
        self.toolbar.update()

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.quit()

    def Checkboxes(self, parent):
        self.var = Tk.BooleanVar()
        c = Tk.Checkbutton(parent, text="FillerText", onvalue="on",offvalue = "off", variable = self.var)
        c.pack()
        print self.var.get()
    
    def cb(self):
        print self.var.get()

def main():
    root = Tk.Tk()
    root.geometry("900x900+300+300")
    app = LCVisualization(root)
    root.update()
    root.deiconify()
    root.mainloop()



if __name__ == '__main__':
   main() 

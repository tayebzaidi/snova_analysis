#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backend_bases import key_press_handler
import numpy as np

import matplotlib.figure
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

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
        self.f = matplotlib.figure.Figure(figsize=(10,9), dpi=80)
        self.ax0 = self.f.add_axes( (0.05, .05, .50, .50), axisbg=(.75,.75,.75), frameon=False)
        self.ax1 = self.f.add_axes( (0.05, .55, .90, .45), axisbg=(.75,.75,.75), frameon=False)
        self.ax2 = self.f.add_axes( (0.55, .05, .50, .50), axisbg=(.75,.75,.75), frameon=False)

        self.ax0.set_xlabel( 'Time (s)' )
        self.ax0.set_ylabel( 'Frequency (Hz)' )
        self.ax0.plot(np.max(np.random.rand(100,10)*10,axis=1),"r-")
        self.ax1.plot(np.max(np.random.rand(100,10)*10,axis=1),"g-")
        self.ax2.pie(np.random.randn(10)*100)    

        self.frame = Tk.Frame( parent )
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
 
        self.canvas = tkagg.FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.show()
     
        self.toolbar = tkagg.NavigationToolbar2TkAgg(self.canvas, self.frame )
        self.toolbar.pack()
        self.toolbar.update()

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.quit()

    def Checkboxes(self, parent):
        self.var = Tk.IntVar()
        c = Tk.Checkbutton(parent, text="FillerText", variable=self.var)
        c.pack()

def main():
    root = Tk.Tk()
    root.geometry("300x300+300+300")
    app = LCVisualization(root)
    root.update()
    root.deiconify()
    root.mainloop()



if __name__ == '__main__':
   main() 

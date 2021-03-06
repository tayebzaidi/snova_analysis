#!/usr/bin/env python
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backend_bases import key_press_handler
from LightcurveClass import Lightcurve
import LightcurveClass
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
import json

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
    
       
        self.ButtonFrame=Tk.Frame(bd=1, relief=Tk.SUNKEN)
        self.ButtonFrame.grid(row=0,padx=5,pady=5, column=0)        
        self.DataFrame = Tk.Frame(bd=1, relief=Tk.SUNKEN, master = self.ButtonFrame)
        self.DataFrame.grid(row=0,padx=5,pady=5)
        self.ToggleFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN, master = self.ButtonFrame)
        self.ToggleFrame.grid(row=1)
        self.RBFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN, master = self.ButtonFrame)
        self.RBFrame.grid(row=2,padx=5,pady=5)
        self.STypeFrame = Tk.Frame(height=2, bd=1, relief=Tk.SUNKEN, master= self.ButtonFrame)  
        self.STypeFrame.grid(row=3, padx=5, pady=5)
        self.JSONFrame = Tk.Frame(height = 2, bd=1, relief = Tk.SUNKEN, master = self.ButtonFrame)
        self.JSONFrame.grid(row=4, padx=5, pady=5)



        #initialize variables here
        self.dataHV = Tk.IntVar()
        self.dataRFrame = Tk.IntVar()
        self.dataDESnoZ = Tk.IntVar()
        self.band = Tk.StringVar()
        self.toggle = Tk.StringVar()
        self.stype = Tk.StringVar()
        self.norm = Tk.IntVar()
        self.sampled = Tk.IntVar()

        self.DataSelect(parent)
        self.GetData()

        self.initFigure(parent)
        self.SplineFitType()
        self.Selection()
        self.Misc()


        # This is where I begin the matplotlib code first initializing the Figure 

    def initFigure(self, parent):
        self.f = matplotlib.figure.Figure(figsize=(7,7), dpi=90)
        self.ax0 = self.f.add_subplot(1,1,1)
        #self.ax0.set_aspect(1)

        self.ax0.set_xlabel( 'Phase (days)' )
        self.ax0.set_ylabel( 'Normalized Flux' )

        self.frame = Tk.Frame(parent)
        self.frame.grid(row=0,padx=5,pady=5, column = 1)

        self.canvas = tkagg.FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0,padx=5,pady=5)
        self.canvas.show()

        toolbar_frame = Tk.Frame(parent)
        toolbar_frame.grid(row=2)
     
        self.toolbar = tkagg.NavigationToolbar2TkAgg(self.canvas, toolbar_frame )
        self.toolbar.update()

        #labels for axes
        #self.ax0.xlabel('Phase', fontsize=18)
        #self.ax0.ylabel('Normalized Flux', fontsize = 16)
        #self.suptitle('L

    # Create method Plot to allow for on the fly adjustment of the plotting
    def Plot(self):
        self.ax0.clear()
        count = 0
        for data in self.splinedat:
            if data['band'] == self.band.get():
                minp = np.array(data['min'])
                maxp = np.array(data['max']) 
                ydata = data['spldata_sampled']
                xdata = data['mjddata_sampled'] 
                label = data['stype']
                if self.toggle.get() != "All":
                    xraw = data['xraw']
                    yraw = data['yraw']
                    
                    #if minp.size > 0:
                    #    self.ax0.scatter(np.array(data['min'])[:,0], np.array(data['min'])[:,1], color='blue')
                    #if maxp.size > 0:
                    #    self.ax0.scatter(np.array(data['max'])[:,0], np.array(data['max'])[:,1], color='red')
                    #self.ax0.errorbar(xraw, yraw, yerr=data['magerr'],fmt='o')
                print self.norm.get()
                print data
                if self.norm.get() == 1:
                    # Normalize the data along the y axis
                    if self.sampled.get() == 1 and len(data['spldata_sampled']) > 1:
                        print data['stype']
                        if data['stype'] != -9:
                            ydata = np.array(data['spldata_sampled'])# - maxp[0][1]
                            xdata = np.array(data['mjddata_sampled'])# - maxp[0][0]
                            count += 1 
                            self.ax0.plot(xdata, ydata)
                    elif len(data['max']) > 0:
                        ydata = data['splinedata']# - maxp[0][1]
                        xdata = data['phase']# - maxp[0][0]
                        xraw = data['xraw'] - maxp[0][0]
                        yraw = data['yraw'] - maxp[0][1]
                        print 'Yay!', maxp[0][1]
                        self.ax0.plot(xdata, ydata)
                        self.ax0.scatter(xraw, yraw)
                #line, = self.ax0.plot(xdata, ydata, picker=self.line_picker, label=label)
                #self.ax0.plot(xdata, ydata)
                ydata = data['splinedata']
                xdata = data['phase']
                #yraw = data['yraw']
                #xraw = data['xraw']
                print data['min']
                print data['max']
                #self.ax0.scatter(data[minp][:,0], minp[:,1], color='blue')
                #self.ax0.scatter(maxp[:,0], maxp[:,1], color='red')
                #self.ax0.plot(xdata, ydata)
                #self.ax0.errorbar(xraw, yraw, yerr=data['magerr'], fmt='o')
                   
        print count        
        self.canvas.show()
        #self.f.canvas.mpl_connect('button_press_event', self.onPick)         
        
            

        #self.ax0.plot([3,2,1])
        #    self.canvas.show()

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def line_picker(self, line, mouseevent):
        if mouseevent.xdata is None: return False, dict()
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        maxd = 0.0005
        d = np.sqrt((xdata-mouseevent.xdata)**2. + (ydata-mouseevent.ydata)**2.)
        ind = np.nonzero(np.less_equal(d, maxd))
        if len(ind):
            pickx = np.take(xdata, ind)
            picky = np.take(ydata, ind)
            props = dict(ind=ind, pickx=pickx, picky=picky, label=line._label)
            return True, props
        else:
            return False, dict()

    #def onPick(self, event):
    #    print('onpick line', event.label)

    def onExit(self):
        self.quit()

    def GetData(self):
        if self.dataHV.get() * self.dataRFrame.get() * self.dataDESnoZ.get() == 1:
            LCR = readin.SNrest()
            LCHV = readin.harvard()
            self.LCRrec = LCR.toRecArray()
            self.LCHVrec = LCHV.toRecArray()
            LC = LightcurveClass.combine2(self.LCHVrec, self.LCRrec)
            self.rec = LC

        elif self.dataHV.get() * self.dataRFrame.get() == 1:
            LCR = readin.SNrest()
            LCHV = readin.harvard()
            self.LCRrec = LCR.toRecArray()
            self.LCHVrec = LCHV.toRecArray()
            LC = LightcurveClass.combine2(self.LCHVrec, self.LCRrec)
            self.rec = LC

        elif self.dataHV.get() == 1:
            LCHV = readin.harvard()
            self.LCHVrec = LCHV.toRecArray()
            self.rec = self.LCHVrec

        elif self.dataRFrame.get() == 1:
            LCR = readin.SNrest()
            self.LCRrec = LCR.toRecArray()
            self.rec = self.LCRrec

        elif self.dataDESnoZ.get() == 1:
            LCDES = readin.DESnoHOSTZ()
            LCDESrec = LCDES.toRecArray()
            self.rec = LCDESrec
        self.BandRadioButtons()

    def PullData(self):
        if self.stype.get() == "UnivariateSpline":
            self.splinedat, length = SplineFit.Usplinefit(self.rec, self.toggle.get(), self.band.get())
        elif self.stype.get() == "nonparam":
            self.splinedat, length = SplineFit.NonParam(self.rec, self.toggle.get(), self.band.get()) 
        elif self.stype.get() == "supersmoother":
            self.splinedat, length = SplineFit.Supersmoother(self.rec, self.toggle.get(), self.band.get())
        else:
            self.splinedat, length = SplineFit.splinefit(self.rec, self.toggle.get(), self.band.get())

    #Define Checkboxes for the Data Selection
    def DataSelect(self, parent):
        self.dataHV.set(1)
        self.dataRFrame.set(1)
        self.dataDESnoZ.set(0)
        Tk.Checkbutton(self.DataFrame, text="HarvardLC", variable = self.dataHV, command = self.datacheck).grid(row=0,padx=5,pady=5) 
        Tk.Checkbutton(self.DataFrame, text="Restframe", variable = self.dataRFrame, command = self.datacheck).grid(row=1)
        Tk.Checkbutton(self.DataFrame, text="DESnoHOSTZ", variable = self.dataDESnoZ, command = self.datacheck).grid(row=2)
        

    def Selection(self):
        self.toggle.set('Single')
        Tk.Radiobutton(self.ToggleFrame, text="Single", variable = self.toggle,value = "Single", command=self.togglecheck).grid(row=0,padx=5,pady=5)
        Tk.Radiobutton(self.ToggleFrame, text="All", variable=self.toggle, value = "All", command = self.togglecheck).grid(row=1,padx=5,pady=5)
        Tk.Radiobutton(self.ToggleFrame, text="Thirty", variable = self.toggle, value = "Thirty", command = self.togglecheck).grid(row=2,padx=5,pady=5)

    def BandRadioButtons(self):
        self.band.set("B")
        try:
            Buttons_tmp = set(self.rec.band)
            
            Buttons = set(self.rec.band)  #Define the Buttons to be a set of all possible bands
            
        except AttributeError:
            Buttons = ['B', 'V', 'R', 'I']
        for i,text in enumerate(Buttons):
            text = Tk.Radiobutton(self.RBFrame, text='Band %s' % text, variable = self.band, value = text,command = self.bandcheck).grid(row=i)

    def SplineFitType(self):
        self.stype.set("Supersmoother")
        Tk.Radiobutton(self.STypeFrame, text="Univariate", variable = self.stype, value = "UnivariateSpline", command = self.sftype).grid(row=0,padx=5,pady=5)
        Tk.Radiobutton(self.STypeFrame, text="Splrep", variable = self.stype, value = "splrep", command = self.sftype).grid(row=1,padx=5,pady=5)
        Tk.Radiobutton(self.STypeFrame, text="NonParam", variable = self.stype, value = "nonparam", command = self.sftype).grid(row=2,padx=5,pady=5)
        Tk.Radiobutton(self.STypeFrame, text="Supersmoother", variable = self.stype, value = "supersmoother", command = self.sftype).grid(row=3, padx=5,pady=5)
        

    def Misc(self):
        Tk.Button(self.JSONFrame, text="Export current data to JSON", command = self.Export).grid(row=0, padx=5, pady=5)
        Tk.Button(self.JSONFrame, text="Plot data", command = self.plot).grid(row=1, padx=5, pady=5)
        Tk.Checkbutton(self.JSONFrame, text = "Move to Origin", command = self.normalize, variable = self.norm).grid(row=2, padx=5, pady=5)
        Tk.Checkbutton(self.JSONFrame, text = 'Sampled Data only', command = self.normalize, variable = self.sampled).grid(row=3, padx=5, pady=5)
        

    #Define the commands all the Buttons are tied to
    
    #Start with the Data Selection commands
    def datacheck(self):
        print self.dataHV.get(), " ", self.dataRFrame.get()
        self.GetData()

    def bandcheck(self):
        print self.band.get()
        #self.Plot()

    def normalize(self):
        print self.norm.get(), self.sampled.get()

    def togglecheck(self):
        print self.toggle.get()
        #self.Plot()

    def sftype(self):
        print self.stype.get()
        self.PullData()

    def plot(self):
        print 'Plotting'
        self.Plot()

    def Export(self):
        print "Exporting"
        f_out = open('SplinedataU', 'w')
        f_out.write(json.dumps(self.splinedat, sort_keys=True, indent=4))
        f_out.close()
        print "Done Exporting"

    

def main():
    root = Tk.Tk()
    #root.geometry("500x1000+300+300")
    app = LCVisualization(root)
    root.update()
    root.deiconify()
    root.mainloop()



if __name__ == '__main__':
   main() 

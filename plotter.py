import matplotlib.pyplot as plt
import sys

def plot1D(x,y,col,show, num_of_figs = 1, linewidth = 1.0, lnstyle = "."): #x is the 1D array of x axis data, y --> y-axis (independent var)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x,y,color = col, linestyle = lnstyle)
    if show == 1:
        Show(fig)
    return fig


def Show(fig):
    plt.show(fig)    
    



if __name__ == '__main__':
    sys.exit()


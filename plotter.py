import matplotlib.pyplot as plt
import sys

def plot1D(x,y,col,figure_number = 1, linewidth = 1.0, lnstyle = ":"): #x is the 1D array of x axis data, y --> y-axis (independent var)
    fig = plt.figure(figure_number)
    ax = fig.add_subplot(figure_number,1,1)
    ax.plot(x,y,color = col, linestyle = lnstyle)
    return fig


def Show():
    plt.show()    
    



if __name__ == '__main__':
    sys.exit()


import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
rc('font', family='roman')



def read_data(fname):
    arr = np.genfromtxt(fname, skip_header=1, usecols=(np.arange(10)*2+1), dtype=float)
    return arr


def graph_four(xset, yset, xsetlabel, ysetlabel, figname = ""):
    plt.plot(xset, yset[0], 'k-', label=ysetlabel[0])
    plt.plot(xset, yset[1], 'r--', label=ysetlabel[1])
    plt.plot(xset, yset[2], 'bo-', label=ysetlabel[2])
    plt.plot(xset, yset[3], 'gs-', label=ysetlabel[3])

    plt.legend(loc=0)

    plt.xlabel(xsetlabel)

    plt.savefig(figname + ".eps")
    #plt.savefig(figname + ".png")
    #plt.show()
    plt.clf()


if __name__ == "__main__":
    d = read_data("MultiCycleTotal.txt")
    d[[1,2]] = d[[1,2]] * d[5]
    d[[3,4]] = d[[3,4]] * d[6]
    d = d[[1,2,3,4]]

    ylabels = ["DU Input Mass", "LWR-TRU Input Mass", "FR-U Input Mass", "FR-TRU Input Mass"]
    graph_four(np.arange(1, 11), d, "Cycle Number", ylabels, figname="input_figs")

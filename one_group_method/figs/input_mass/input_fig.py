import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
rc('font', family='roman')

linestyles = ['k-', 'r--', 'bo-', 'gs-']

def read_data(fname):
    arr = np.genfromtxt(fname, skip_header=1, usecols=(np.arange(10)*2+1), dtype=float)
    return arr


def graph_data(xset, yset, xsetlabel, ysetlabel, figname="", yaxislabel=None, ax=None):
    for i, ydata in enumerate(yset):
        plt.plot(xset, ydata, linestyles[i], label=ysetlabel[i])

    plt.legend(loc=0)

    plt.xlabel(xsetlabel)
    if yaxislabel is not None:
        plt.ylabel(yaxislabel)

    if ax is not None:
        plt.axis(ax)

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
    graph_data(np.arange(1, 11), d, "Cycle Number", ylabels, figname="input_figs")


    d = read_data("MultiCycleTotal.txt")
    d = d[[8]]
    graph_data(np.arange(1, 11), d, "Cycle Number", ["LWR UF Needed [kg]"], 
               "lwr_uf_needed", "LWR UF Mass Needed [kg]", [1, 10, 0, 26])

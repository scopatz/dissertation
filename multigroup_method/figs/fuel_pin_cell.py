import matplotlib
from matplotlib.patches import Circle, Arrow
from matplotlib.collections import PatchCollection
import pylab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
rc('font', family='roman')


fig=pylab.figure()
ax=fig.add_subplot(111, aspect='equal')

resolution = 50 # the number of vertices

radii = [0.477, 0.4185, 0.41]
patches = [Circle((0.0, 0.0), r, edgecolor='k') for r in radii] + \
          [Arrow(0.0, 0.0, r*np.cos(i*np.pi/6), r*np.sin(i*np.pi/6), width=0.05, facecolor='k', linewidth=10.0) for i, r in enumerate(radii[::-1])]


colors = [90, 30, 100, 0, 0, 0]
p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.80)
p.set_array(pylab.array(colors))
ax.add_collection(p)
ax.axis([-0.65635, 0.65635, -0.65635, 0.65635])

rnames = ['fuel', 'void', 'clad']
for i, r, n in zip(range(len(rnames)), radii[::-1], rnames):
    plt.text((r/3), (r*i/(3+0.1*(i+1)))*np.sin(i*np.pi/6) - 0.04, "$r_{{\\mbox{{{0}}}}}$ = {1}".format(n, r), size='xx-small')

plt.plot([-0.65635, 0.65635], [-(radii[0] + 0.65635)/2]*2, 'k-')
plt.text(-0.1, -(radii[0] + 0.65635)/2 - 0.03, "pitch = {0}".format(0.65635*2), size='small')

plt.xlabel("x [cm]")
plt.ylabel("y [cm]")

plt.savefig("fuel_pin_cell.eps")

pylab.show()

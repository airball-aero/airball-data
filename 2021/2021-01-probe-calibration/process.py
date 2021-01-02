#!/usr/bin/python
# coding=utf-8

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np
import scipy.optimize as spo

########################################################################

# Plot flow data versus pressure ratios

def plotpressures(ra0, rb0, flow_data, pov_angle, var_name, title, filename):
    def radius(a, b):
        return a * a + b * b
    r = np.vectorize(radius)(ra0, rb0)

    color_dimension = r
    minn, maxx = color_dimension.min(), color_dimension.max()
    norm = matplotlib.colors.Normalize(minn, maxx)
    m = matplotlib.cm.ScalarMappable(norm=norm, cmap='jet')
    m.set_array([])
    fcolors = m.to_rgba(color_dimension)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('dpa / dp0')
    ax.set_ylabel('dpb / dp0')
    ax.set_zlabel(var_name)
    ax.plot_surface(
        ra0,
        rb0,
        flow_data,
        rstride=1, cstride=1,
        facecolors=fcolors)
    fake2Dline = matplotlib.lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
    ax.legend([fake2Dline], [title], numpoints = 1)
    ax.view_init(30, pov_angle)
    plt.savefig(filename, dpi=600)

########################################################################    

# Plot calibration surfaces for a probe configuration with the given
# "raw2data" function.

def plot_calibration(name, raw2data):
    ra0 = np.arange(-1.25, 1.25, .025)
    rb0 = np.arange(-1.25, 1.25, .025)
    ra0, rb0 = np.meshgrid(ra0, rb0)

    def alphabeta(ra0, rb0):
        r = raw2data(1.0, ra0, rb0)
        return (math.degrees(r[0]), math.degrees(r[1]), r[2])

    (alpha, beta, q) = np.vectorize(alphabeta)(ra0, rb0)

    plotpressures(ra0, rb0, alpha, 85,
                  "alpha (degrees)",
                  name + " alpha versus pressure ratios",
                  name + "_alpha_vs_ratios.png")
    plotpressures(ra0, rb0, beta, 15,
                  "beta (degrees)",                  
                  name + " beta versus pressure ratios",
                  name + "_beta_vs_ratios.png")
    plotpressures(ra0, rb0, q, 85,
                  "q/ dp0",
                  name + " (q / dp0) versus pressure ratios",
                  name + "_q_over_dp0_vs_ratios.png")

########################################################################

# Plot calibration surfaces for v1 and v2 probes.

plot_calibration("v1", v1_probe_raw2data)
plot_calibration("v2", v2_probe_raw2data)

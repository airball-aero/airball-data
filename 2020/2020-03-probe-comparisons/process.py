#!/usr/bin/python
# coding=utf-8

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np
import scipy.optimize as spo

########################################################################

# This is the core formula that computes the pressure at a given point
# on a sphere as a function of angular offset from the stagnation point.
# The result is a ratio of the stagnation pressure _q_. The angle is
# given in radians.

def sphere_pressure_coefficient_polar(angle):
    def cos_sq(x):
        y = math.cos(x)
        return y * y
    return 1.0 - 9.0 / 4.0 * cos_sq(angle - math.pi / 2.0);

# This formula takes two angles, alpha and beta, and computes the
# pressure coefficient at the given point using the distance formula.

def sphere_pressure_coefficient_cartesian(alpha, beta):
    return sphere_pressure_coefficient_polar(
        math.sqrt(alpha * alpha + beta * beta))

########################################################################

# Subsequent functions refer to two probe geometries. These are:
#
# ** Probe v1 **
#
# This is a 5-hole sphere plus a static source. The raw measurements are:
#     (dp0, dpA, dpB)
# where the pressures are defined as:
#     dp0 = (center hole) - (static)
#     dpA = (lower hole) - (upper hole)
#     dpB = (right hole) - (left hole)
#
# ** Probe v2 **
#
# This is a 5-hole probe where the static pressure is inferred from one
# hole on the centerline at 90 degrees from the centerline, on the bottom
# of the spherical nose. The raw measurements are:
#     (dp0, dpA, dpB)
# where the pressures are defined as:
#     dp0 = (center hole) - (bottom 90 degree hole)
#     dpA = (lower hole) - (upper hole)
#     dpB = (right hole) - (left hole)

########################################################################

# The following functions takes a triple of airflow parameters
#     (alpha, beta, q)
# where alpha and beta are in radians, and q can be in any units but,
# for the purposes of this module, we always use pascals. They return
# the expected "raw" measurements from potential flow theory.

# Probe v1 version

def v1_probe_data2raw(alpha, beta, q):
    p0 = q * sphere_pressure_coefficient_cartesian(
        alpha,
        beta)
    pUpr = q * sphere_pressure_coefficient_cartesian(
        alpha - math.pi / 4,
        beta)
    pLwr = q * sphere_pressure_coefficient_cartesian(
        alpha + math.pi / 4,
        beta)
    pLft = q * sphere_pressure_coefficient_cartesian(
        alpha,
        beta - math.pi / 4)
    pRgt = q * sphere_pressure_coefficient_cartesian(
        alpha,
        beta + math.pi / 4)
    return [p0, pLwr - pUpr, pRgt - pLft]

# Probe v2 version

def v2_probe_data2raw(alpha, beta, q):
    p0 = q * sphere_pressure_coefficient_cartesian(
        alpha,
        beta)
    pUpr = q * sphere_pressure_coefficient_cartesian(
        alpha - math.pi / 4,
        beta)
    pLwr = q * sphere_pressure_coefficient_cartesian(
        alpha + math.pi / 4,
        beta)
    pBtm = q * sphere_pressure_coefficient_cartesian(
        alpha + math.pi / 2,
        beta)
    pLft = q * sphere_pressure_coefficient_cartesian(
        alpha,
        beta - math.pi / 4)
    pRgt = q * sphere_pressure_coefficient_cartesian(
        alpha,
        beta + math.pi / 4)
    return [p0 - pBtm, pLwr - pUpr, pRgt - pLft]

########################################################################

# The following functions take a triple of raw pressure measurements
#     (dp0, dpa, dpb)
# where these pressures can be in any units but, for the purposes of
# this module, we always use pascals. They return the airdata parameters
#     (alpha, beta, q)
# from potential flow theory.

# Generic case version

def generic_probe_raw2data(dp0, dpa, dpb, data2raw):

    ra0 = dpa / dp0
    rb0 = dpb / dp0

    def to_optimize(angles):
        [dp0, dpa, dpb] = data2raw(angles[0], angles[1], 1.0)
        return [dpa / dp0 - ra0, dpb / dp0 - rb0]

    [alpha, beta] = spo.root(to_optimize, [0, 0]).x
    dp0_over_q = data2raw(alpha, beta, 1.0)[0]
    q = dp0 / dp0_over_q

    return [alpha, beta, q]

# Probe v1 version

def v1_probe_raw2data(dp0, dpa, dpb):
    return generic_probe_raw2data(dp0, dpa, dpb, v1_probe_data2raw)
    
# Probe v2 version

def v2_probe_raw2data(dp0, dpa, dpb):
    return generic_probe_raw2data(dp0, dpa, dpb, v2_probe_data2raw)

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

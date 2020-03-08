#!/usr/bin/python

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np

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

# The following functions takes a triple of airflow parameters
#     (alpha, beta, q)
# where alpha and beta are in radians, and q can be in any units but,
# for the purposes of this module, we always use pascals. They return
# the expected "raw" measurements from potential flow theory.

# This function is for a "v1" 5-hole probe configuration that consists
# of a 5-hole sphere plus a static source. The raw measurements are:
#     (dp0, dpA, dpB)
# where the pressures are defined as:
#     dp0 = (center hole) - (static)
#     dpA = (lower hole) - (upper hole)
#     dpB = (right hole) - (left hole)

def v1_probe_data2raw(alpha, beta, q):
    p0 =  q * sphere_pressure_coefficient_cartesian(
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
    return (p0, pLwr - pUpr, pRgt - pLft)

# This function is for a "v2" 5-hole probe where the static pressure
# is inferred from one hole on the centerline at 90 degrees from the
# centerline, and so does not have a simple aerodynamic static source.
# The raw measurements are:
#     (dp0, dpA, dpB)
# where the pressures are defined as:
#     dp0 = (center hole) - (bottom 90 degree hole)
#     dpA = (lower hole) - (upper hole)
#     dpB = (right hole) - (left hole)

def v2_probe_data2raw(alpha, beta, q):
    p0 =  q * sphere_pressure_coefficient_cartesian(
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
    return (p0 - pBtm, pLwr - pUpr, pRgt - pLft)

########################################################################

alpha = np.arange(-25.0, 25.5, .5)
beta  = np.arange(-25.0, 25.5, .5)
alpha, beta = np.meshgrid(alpha, beta)

def pressures(a, b):
    return v2_probe_data2raw(
        math.radians(a),
        math.radians(b),
        1.0)

dp0, dpA, dpB = np.vectorize(pressures)(alpha, beta)

def ratio_a(a, b):
    dp0, dpA, dpB = v2_probe_data2raw(
        math.radians(a),
        math.radians(b),
        1.0)
    return dpA / dp0

def ratio_b(a, b):
    dp0, dpA, dpB = v2_probe_data2raw(
        math.radians(a),
        math.radians(b),
        1.0)
    return dpB / dp0

dpRA = np.vectorize(ratio_a)(alpha, beta)
dpRB = np.vectorize(ratio_b)(alpha, beta)

def plotpressures(alpha, beta, pressures, angle, title, filename):
    def radius(a, b):
        return a * a + b * b
    r = np.vectorize(radius)(alpha, beta)

    color_dimension = r
    minn, maxx = color_dimension.min(), color_dimension.max()
    norm = matplotlib.colors.Normalize(minn, maxx)
    m = matplotlib.cm.ScalarMappable(norm=norm, cmap='jet')
    m.set_array([])
    fcolors = m.to_rgba(color_dimension)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('alpha (degrees)')
    ax.set_ylabel('beta (degrees)')
    ax.plot_surface(
        alpha,
        beta,
        pressures,
        rstride=1, cstride=1,
        facecolors=fcolors)
    fake2Dline = matplotlib.lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o')
    ax.legend([fake2Dline], [title], numpoints = 1)
    ax.view_init(30, angle)
    plt.savefig(filename, dpi=600)

plotpressures(alpha, beta, dp0, 85, "dp0 / q", "dp0_over_q.png")

plotpressures(alpha, beta, dpA, 85, "dpA / q", "dpA_over_q.png")
plotpressures(alpha, beta, dpB, 15, "dpB / q", "dpB_over_q.png")

plotpressures(alpha, beta, dpRA, 85, "dpA / dp0", "dpA_over_dp0.png")
plotpressures(alpha, beta, dpRB, 15, "dpB / dp0", "dpB_over_dp0.png")

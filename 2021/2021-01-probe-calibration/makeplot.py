#!/usr/bin/python

from mpl_toolkits import mplot3d
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
import pickle

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

def v2_probe_theoretical(alpha, beta, scaling=1.0):
    alpha = math.radians(alpha)
    beta = math.radians(beta)    
    p0 = sphere_pressure_coefficient_cartesian(
        alpha,
        beta)
    pUpr = sphere_pressure_coefficient_cartesian(
        alpha - math.pi / 4,
        beta)
    pLwr = sphere_pressure_coefficient_cartesian(
        alpha + math.pi / 4,
        beta)
    pBtm = sphere_pressure_coefficient_cartesian(
        alpha + math.pi / 2,
        beta)
    pLft = sphere_pressure_coefficient_cartesian(
        alpha,
        beta - math.pi / 4)
    pRgt = sphere_pressure_coefficient_cartesian(
        alpha,
        beta + math.pi / 4)
    return {
        'dp0_q': scaling * (p0 - pBtm),
        'dpA_q': scaling * (pUpr - pLwr),
        'dpB_q': scaling * (pRgt - pLft),
    }

########################################################################

def read(filename):
    results = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for k in reader.fieldnames: results[k] = []
        for row in reader:
            if float(row['dp0']) != 0.0:
                for k in row.keys():
                    results[k].append(float(row[k]))
    return results

########################################################################

def air_density(p, t_degC):
    t_K = t_degC + 273.15
    return p / (287.058 * t_K)

def speed_from_mph(mph):
    return mph * 0.44704

def q(p, t_degC, mph):
    return 0.5 * air_density(p, t_degC) * (speed_from_mph(mph) ** 2)

def calculate_ratios(d):
    d['q'] = []
    d['dp0_q'] = []
    d['dpA_q'] = []
    d['dpB_q'] = []        
    for i in range(0, len(d['seq'])):
        d['q'].append(q(d['baro'][i], d['oat'][i], d['mph'][i]))
    for i in range(0, len(d['seq'])):
        d['dp0_q'].append(d['dp0'][i] / d['q'][i])
        d['dpA_q'].append(d['dpA'][i] / d['q'][i])
        d['dpB_q'].append(d['dpB'][i] / d['q'][i])        

def reduce_average(d, column_names):
    reduced = {}
    for i in range(0, len(d['seq'])):
        k = (d['alpha'][i], d['beta'][i])
        if not reduced.get(k):
            reduced[k] = {}
            for n in column_names:
                reduced[k][n] = {
                    'count': 0,
                    'total': 0.0,
                }
                reduced[k][n]['count'] = reduced[k][n]['count'] + 1
                reduced[k][n]['total'] = reduced[k][n]['total'] + d[n][i]
    r = {
        'alpha': [],
        'beta': [],
    }
    for n in column_names:
        r[n] = []
    for k in reduced.keys():
        r['alpha'].append(k[0])
        r['beta'].append(k[1])
        for n in column_names:
            r[n].append(reduced[k][n]['total'] / reduced[k][n]['count'])
    r['q'] = d['q']
    return r
        
########################################################################

def add_theoreticals(r):
    r['dp0_q_th'] = []
    r['dpA_q_th'] = []
    r['dpB_q_th'] = []
    for i in range(0, len(r['alpha'])):
        th = v2_probe_theoretical(r['alpha'][i], r['beta'][i])
        r['dp0_q_th'].append(th['dp0_q'])
        r['dpA_q_th'].append(th['dpA_q'])
        r['dpB_q_th'].append(th['dpB_q'])

########################################################################

def add_ratios(r):
    vars = ['dp0_q', 'dpA_q', 'dpB_q']
    for v in vars:
        r[v + '_ratio'] = []
    for i in range(0, len(r['alpha'])):
        for v in vars:
            try:
                r[v + '_ratio'].append(r[v][i] / r[v + '_th'][i])
            except:
                r[v + '_ratio'].append(0)
        
########################################################################

def compute_dataset(filename):
    d = read(filename)
    calculate_ratios(d)
    r = reduce_average(d, ['dp0_q', 'dpA_q', 'dpB_q'])
    add_theoreticals(r)
    add_ratios(r)
    return r

########################################################################

def compare_data_theory(r):
    for v in ['dp0_q', 'dpA_q', 'dpB_q']:

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('alpha (degrees)')
        ax.set_ylabel('beta (degrees)')
        ax.set_zlabel(v + ' (data / theory)')
        p = ax.scatter3D(r['alpha'], r['beta'], r[v + '_ratio'])
        ax.legend([p], [v + ' (data / theory)'])
        plt.savefig(v + '_data_theory_ratio.png', dpi=600)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('alpha (degrees)')
        ax.set_ylabel('beta (degrees)')
        ax.legend([
            ax.scatter3D(r['alpha'], r['beta'], r[v]),
            ax.scatter3D(r['alpha'], r['beta'], r[v + '_th']),
        ], [
            v + ' data',
            v + ' theory',
        ])
        plt.savefig(v + '_data_vs_theory.png', dpi=600)

########################################################################

def compute_error(r, v, s):
    err = 0.0
    for i in range(0, len(r['alpha'])):
        if v == 'dpA_q' and r['alpha'][i] == 0:
            continue
        if v == 'dpB_q' and r['beta'][i] == 0:
            continue
        th = v2_probe_theoretical(r['alpha'][i], r['beta'][i], s)[v]
        e = r[v][i] - th
        err = err + (e * e)
    return err

def plot_scaling(r, v):
    scalings = []
    errors = []
    for s in np.arange(0.1, 1.9, 0.05):
        scalings.append(s)
        errors.append(compute_error(r, v, s))
    fig, (ax1) = plt.subplots(1)
    ax1.plot(scalings, errors)
    ax1.set(
        title=v + ' effect of scaling',
        xlabel="Scaling applied to theory",
        ylabel='Total squared error b/w data and theory')
    ax1.xaxis.set_ticks(np.arange(0.1, 1.9, 0.1))
    ax1.grid(b=True, which='both', axis='both')
    plt.savefig(v + '_error_vs_scaling.png', dpi=600)

def plot_scalings(r):
    for v in ['dp0_q', 'dpA_q', 'dpB_q']:
        plot_scaling(r, v)

########################################################################
    
r = compute_dataset(sys.argv[1])
compare_data_theory(r)
plot_scalings(r)

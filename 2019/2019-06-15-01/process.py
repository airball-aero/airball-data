#!/usr/bin/python

import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from numpy import convolve
import bisect

########################################################################

def pressure_count_to_value_hsc(count, fss, is_gage):
    p_min = 0 if is_gage else -fss
    p_max = fss
    n_ratio = (count * 1.0) / (pow(2, 14) * 1.0)
    return p_min + 1.25 * (n_ratio - 0.1) * (p_max - p_min)

def strings_to_floats(strings):
    r = []
    for s in strings:
        r.append(float(s))
    return r
        
def read(filehandle, cols):

    result = {}
    for col in cols:
        result[col] = []

    for row in csv.reader(filehandle, delimiter=','):
        try:
            r = strings_to_floats(row)
        except:
            continue
        if len(r) < len(cols):
            continue
        for i in range(0, len(cols)):
            result[cols[i]].append(r[i])

    return result

########################################################################

def read_pressures():

    (cin, cout) = os.popen2('cat data.csv | grep \',p\' | sed \'s/,p//g\'')
    dataset = read(cout, ['time', 'c0', 'c1', 'c2'])
    
    convert = lambda c: pressure_count_to_value_hsc(c, 4000, False)
    dataset['p0'] = map(convert, dataset['c0'])
    dataset['p1'] = map(convert, dataset['c1'])
    dataset['p2'] = map(convert, dataset['c2'])

    dataset['time'] = map(lambda x: x / 1000 / 60 / 60, dataset['time'])
    
    return dataset

########################################################################

pressures = read_pressures()

plt.subplot(3, 1, 1)
plt.plot(pressures['time'], pressures['p0'])
plt.ylabel('pressure (Pa)')
plt.xlabel('time (h)')

plt.subplot(3, 1, 2)
plt.plot(pressures['time'], pressures['p1'])
plt.ylabel('pressure (Pa)')
plt.xlabel('time (h)')

plt.subplot(3, 1, 3)
plt.plot(pressures['time'], pressures['p2'])
plt.ylabel('pressure (Pa)')
plt.xlabel('time (h)')

plt.savefig('sensor_drift_vs_time.png')

#!/usr/bin/python

import math
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from numpy import convolve
import bisect

########################################################################

def movingaverage(values, window):
    weights = np.repeat(1.0, window) / window
    return np.convolve(values, weights, 'valid')

def movingaverage_dataset(dataset, window):
    firstvar = ''
    result = {}
    
    for key in dataset.keys():
        if key != 'time':
            result[key] = movingaverage(dataset[key], window)
            if firstvar == '':
                firstvar = key
                
    result['time'] = dataset['time'][len(dataset['time']) - len(dataset[firstvar]):]

    return result

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

    telemetry_to_airdata = '../../../airball-embedded/host/build/display/telemetry_to_airdata'
    qnh = 102133.48 # flight barometer setting in Pascals
    variables = [
        'time',
        'rssi',
        'seq',
        'baro',
        'temp',
        'dp0',
        'dpa',
        'dpb',
        'alt',
        'climb',
        'q',
        'ias',
        'tas',
        'alpha',
        'beta',
    ]

    (cin, cout) = os.popen2('%s %f < airdata_20191231_191739.csv' % (telemetry_to_airdata, qnh))
    return read(cout, variables)

########################################################################

def subset_by_independent_variable(dataset, independent_variable, start, end):
    minval = min(dataset[independent_variable])
    maxval = max(dataset[independent_variable])
    istart = bisect.bisect_left(dataset[independent_variable], start)
    iend = bisect.bisect_right(dataset[independent_variable], end)
    result = {}
    for col in dataset.keys():
        result[col] = dataset[col][istart:iend]
    return result

########################################################################

def minimize_dataset_times(datasets):
    min_times = []
    for dataset in datasets:
        min_times.append(min(dataset['time']))
    min_time = min(min_times)
    for dataset in datasets:
        dataset['time'] = map(lambda x: x - min_time, dataset['time'])

########################################################################

# q = 1/2 * rho * v^2
# v = sqrt(2 * q / rho)

def q_to_ias(q):
    air_density = 1.225 # kg/m3
    return math.sqrt(2 * q / air_density)

def mps_to_knots(mps):
    return mps * 1.94384

########################################################################

pressures = read_pressures()

minimize_dataset_times([pressures])
flight_start = 610.0
flight_end = 3218.0
pressures = subset_by_independent_variable(pressures, 'time', flight_start, flight_end)
minimize_dataset_times([pressures])

plt.plot(pressures['time'], map(mps_to_knots, map(q_to_ias, pressures['dp0'])), label="Primitive IAS from dp0")
plt.plot(pressures['time'], map(mps_to_knots, pressures['ias']), label="Fancy IAS from Airball math")

plt.xlabel('Time (s)')
plt.ylabel('IAS (knots)')

plt.legend()
plt.show()

#!/usr/bin/python

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

def read_accels():

    with open('accelerometer-log.csv') as fh:
        accels = read(fh, ['time', 'ax', 'ay', 'az'])

    accels['time'] = map(lambda x: x * 1.0 / 1e+09, accels['time'])
    
    return accels

########################################################################

def read_pressures():

    telemetry_to_airdata = '../../../airball-embedded/host/build/display/telemetry_to_airdata'
    qnh = 100812.79 # flight barometer setting in Pascals
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

    (cin, cout) = os.popen2('%s %f < telemetry-log.csv' % (telemetry_to_airdata, qnh))
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

accels = read_accels()
pressures = read_pressures()

minimize_dataset_times([accels, pressures])

pressures = movingaverage_dataset(pressures, 20)
accels = movingaverage_dataset(accels, 120)

flight_start = 1980.0
flight_end = 4275.0

pressures = subset_by_independent_variable(pressures, 'time', flight_start, flight_end)
accels = subset_by_independent_variable(accels, 'time', flight_start, flight_end)

plt.plot(pressures['time'], map(lambda x: x * 57.2958, pressures['beta']), label="Beta")
plt.plot(accels['time'], map(lambda x: x * -100.0, accels['ay']), label="Y accel")
plt.xlabel('Time (s)')
plt.ylabel('Beta (degrees) or Y accel (g * 100)')
plt.legend()
plt.show()

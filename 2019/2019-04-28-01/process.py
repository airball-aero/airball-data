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

def calibrate_accel_values(values, calibs):

    result = []
    
    def calibrate(value, calibs):
        offset = 0.5 * (calibs[0] + calibs[1])
        gain = 0.5 * (calibs[1] - calibs[0])
        return (value - offset) / gain

    for i in range(0, len(values)):
        result.append(calibrate(values[i], calibs))

    return result

def read_accels():

    # Accel Minimums: -257  -251  -262
    # Accel Maximums: 259  274  234
    
    accel_calibs = {
        'ax': [ -257, 259 ],
        'ay': [ -251, 274 ],
        'az': [ -262, 234 ],
    }

    with open('accelerometer-log.csv') as fh:
        accels = read(fh, ['time', 'ax', 'ay', 'az'])

    # Acceleration times are stored in milliseconds -- normalize to seconds
    for i in range(0, len(accels['time'])):
        accels['time'][i] = float(accels['time'][i]) / float(1000)

    accels['ax'] = calibrate_accel_values(accels['ax'], accel_calibs['ax'])
    accels['ay'] = calibrate_accel_values(accels['ay'], accel_calibs['ay'])
    accels['az'] = calibrate_accel_values(accels['az'], accel_calibs['az'])

    accels['ax'] = movingaverage(accels['ax'], 100)
    accels['ay'] = movingaverage(accels['ay'], 100)
    accels['az'] = movingaverage(accels['az'], 100)
    accels['time'] = accels['time'][len(accels['time']) - len(accels['ax']):]

    return accels

########################################################################

def read_pressures():

    qnh = 101117.57 # flight barometer setting in Pascals
    (cin, cout) = os.popen2('../../../airball-embedded/host/build/display/telemetry_to_airdata %f < telemetry-log.csv' % qnh)
    return read(cout, ['time', 'rssi', 'seq', 'baro', 'temp', 'dp0', 'dpa', 'dpb', 'alt', 'climb', 'q', 'ias', 'tas', 'alpha', 'beta'])

########################################################################

def subset_ivar(dataset, ivar, start, end):
    minval = min(dataset[ivar])
    maxval = max(dataset[ivar])
    istart = bisect.bisect_left(dataset[ivar], start)
    iend = bisect.bisect_right(dataset[ivar], end)
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
        time_col = dataset['time']
        for i in range(0, len(time_col)):
            time_col[i] = time_col[i] - min_time

########################################################################

accels = read_accels()
pressures = read_pressures()

minimize_dataset_times([accels, pressures])

# Show the fact that the Y acceleration seems out of sync with what is
# to be expected -- even during the time when we were on the ground,
# there were variations that we cannot explain.

plt.subplot('211')
plt.plot(
    pressures['time'],
    map(lambda x: x * 3.28084, pressures['alt']))
plt.xlabel('time (s)')
plt.ylabel('altitude (ft)')
plt.subplot('212')
plt.plot(accels['time'], accels['ay'])
plt.xlabel('time (s)')
plt.ylabel('Y acceleration (g)')
plt.savefig('y_acceleration_and_altitude.png')
plt.close()

# Now zero in on the region of interest in the flight.

pressures = subset_ivar(pressures, 'time', 1990, 3125)
accels = subset_ivar(accels, 'time', 1990, 3125)

plt.plot(
    map(lambda x: x * 1.94384, pressures['ias']),
    map(lambda x: x * 57.2958, pressures['alpha']),
    'ro')
plt.xlabel('IAS (knots)')
plt.ylabel('AoA (degrees)')
plt.savefig('ias_vs_aoa.png')
plt.close()

plt.plot(
    pressures['q'],
    map(lambda x: x * 57.2958, pressures['alpha']),
    'ro')
plt.xlabel('dynamic pressure (Pa)')
plt.ylabel('AoA (degrees)')
plt.savefig('ias_vs_q.png')
plt.close()

plt.subplot('411')
plt.plot(
    pressures['time'],
    map(lambda x: x * 3.28084, pressures['alt']))
plt.xlabel('time (s)')
plt.ylabel('altitude (ft)')
plt.subplot('412')
plt.plot(
    pressures['time'],
    map(lambda x: x * 1.94384, pressures['ias'])) 
plt.xlabel('time (s)')
plt.ylabel('IAS (knots)')
plt.subplot('413')
plt.plot(
    pressures['time'],
    map(lambda x: x * 57.2958, pressures['alpha']))
plt.xlabel('time (s)')
plt.ylabel('AoA (deg)')
plt.subplot('414')
plt.plot(
    pressures['time'],
    map(lambda x: x * 57.2958, pressures['beta']))
plt.xlabel('time (s)')
plt.ylabel('yaw (deg)')
plt.savefig('alt_ias_alpha_beta.png')
plt.close()

#!/usr/bin/python

import matplotlib.pyplot as plt

import csv

lines = [
    [float(line[0]) / 3600.0, float(line[3]) / 1000.0]
    for line in csv.reader(open('./battery_draindown.log'))
]

t0 = lines[0][0]

t = [x[0] - t0 for x in lines]
v = [x[1] for x in lines]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('time (hours)')
ax.set_ylabel('battery voltage (volts)')
ax.hlines([3.25, 4.15], t[0], t[-1], colors='orange', linestyle='dashed')
ax.vlines([0, 19], 2.5, 4.3, colors='orange', linestyle='dashed')
ax.scatter(t, v, color='black', marker='.')
plt.title('\n'.join([
    'Probe 18650 3400mAH Panasonic',
    '4.15V to 3.25V, 0 to 19 hours',
]))
plt.savefig('battery-life.png', dpi=600)

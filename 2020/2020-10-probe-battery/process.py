#!/usr/bin/python

import csv
import matplotlib.pyplot as plt

def read_results(filename):
    result = {}
    result['time'] = []
    result['voltage'] = []
    result['current'] = []
    start = -1
    for row in csv.reader(open(filename), delimiter=','):
        time = float(row[0]) / 3600.0
        if start < 0:
            start = time
            time = 0.0
        else:
            time = time - start
        result['time'].append(time)
        result['voltage'].append(float(row[2]))
        result['current'].append(float(row[3]))
    return result

def plot(filename):
    result = read_results(filename + '.csv')
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(
        result['time'],
        result['voltage'])
    ax1.set(
        xlabel="Time (hours)",
        ylabel='Voltage (mV)')
    ax2.plot(
        result['time'],
        result['current'])
    ax2.set(
        xlabel="Time (hours)",
        ylabel='Current (mA)')
    plt.gcf().set_size_inches(11.0, 8.5)
    plt.savefig(filename + '.png', dpi=300)
    
plot('battery-drain')

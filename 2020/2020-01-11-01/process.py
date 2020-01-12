#!/usr/bin/python

import matplotlib.pyplot as plt

probe_static = [
    [ 79, 79, 91, 93, 93, 92, 91, 92, 90, 88, 86, 87, 87, 88, 87, 96, 94, 95, 94, 92, 94, 94, 93, 95, 95, 60, 87, 60, 62, 68, 71, 54 ],
    [ 70, 69, 80, 80, 81, 79, 78, 82, 77, 76, 75, 75, 76, 76, 75, 83, 82, 82, 82, 81, 81, 82, 81, 82, 82, 70, 75, 57, 59, 64, 67, 52 ],
]

alternate_static = [
    [ 74, 70, 90, 66, 60, 92, 95 ],
    [ 68, 66, 80, 62, 57, 80, 83 ],
]

plt.scatter(
    alternate_static[0],
    alternate_static[1],
    label="Alternate static",
    color="blue",
    marker="o")
plt.scatter(
    probe_static[0],
    probe_static[1],
    label="Probe static",
    color="red",
    marker="v")
plt.plot(
    [50, 100],
    [50, 100],
    color="black")

plt.xlabel('N291DR ASI reading (kias)')
plt.ylabel('Airball ASI reading (kias)')

plt.legend()
plt.show()

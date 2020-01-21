#!/usr/bin/python

import matplotlib.pyplot as plt
import math

def in_h2o_to_kias(x):
    # Convert to SI units
    pascals = 248.84 * x
    # P = 1/2 * rho * v^2
    # v = sqrt(2 * P / rho)
    # rho = 1.225 kg/m^3
    v = math.sqrt(2 * pascals / 1.225)
    return v * 1.968505

probe_static = [
    [ 79, 79, 91, 93, 93, 92, 91, 92, 90, 88, 86, 87, 87,
      88, 87, 96, 94, 95, 94, 92, 94, 94, 93, 95, 95, 60, 87, 60, 62,
      68, 71, 54, ],
    [ 70, 69, 80, 80, 81, 79, 78, 82, 77, 76, 75, 75, 76,
      76, 75, 83, 82, 82, 82, 81, 81, 82, 81, 82, 82, 70, 75, 57, 59,
      64, 67, 52, ],
]

alternate_static = [
    [ 74, 70, 90, 66, 60, 92, 95, ],
    [ 68, 66, 80, 62, 57, 80, 83, ],
]

long_pole = [
    [ 77, 92, 86, 83, 74, 62, 57, 54, 48, 45, 42, 43, 46, 50, 53, 56, 60, 66, 67,
      73, 79, 91, 95, 96, 95, 94, 75, 49, 46, 44, 41, 40, 38, 34, 32, 30, 30, ],
    [ 71, 82, 77, 75, 71, 60, 56, 52, 48, 46, 44, 43, 45, 47, 50, 53, 56, 61, 61,
      66, 71, 80, 84, 86, 85, 83, 70, 50, 48, 46, 45, 44, 43, 41, 39, 37, 36, ],
]

manometer_test = [
    [ 1,  2,  3,  4,  5,  6,   7,   7.5,  8,   9,  10 ],
    [40, 54, 68, 77, 87, 96, 103, 106,  110, 117, 124 ],
]

manometer_test[0] = map(in_h2o_to_kias, manometer_test[0])

for i in range(0, len(manometer_test[0])):
    print("%0.2f -> %0.2f" % (manometer_test[0][i], manometer_test[1][i]))

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
plt.scatter(
    long_pole[0],
    long_pole[1],
    label="Long pole",
    color="green",
    marker="x")
plt.plot(
    [25, 100],
    [25, 100],
    color="lightgrey")

plt.xlabel('N291DR ASI reading (kias)')
plt.ylabel('Airball ASI reading (kias)')

plt.legend()
plt.show()

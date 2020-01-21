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

manometer_test = [
    [ 1,  2,  3,  4,  5,  6,   7,   7.5,  8,   9,  10 ],
    [40, 54, 68, 77, 87, 96, 103, 106,  110, 117, 124 ],
]

manometer_test[0] = map(in_h2o_to_kias, manometer_test[0])

plt.scatter(
    manometer_test[0],
    manometer_test[1],
    label="Manometer test",
    color="blue",
    marker="o")
plt.plot(
    [25, 125],
    [25, 125],
    color="lightgrey")

plt.xlabel('Manometer applied dynamic pressure (kias)')
plt.ylabel('Airball ASI reading (kias)')

plt.legend()
plt.show()

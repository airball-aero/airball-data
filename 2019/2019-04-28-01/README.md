# Introduction

This is data from a short test flight with an accelerometer and the
airdata probe, as documented at:

http://www.airball.aero/2019/04/accelerometer-and-airdata-comparison.html

The altimeter setting was 29.86 in Hg = 101117.57 Pascals.

The program `read_serial.py` was what we used to read serial data from
the accelerometer (sent by the Arduino) and print to `stdout`. The
data from the probe was collected using the `log_telemetry` program
from the main repo.

The raw data is in two files, where the timestamps are synchronized
since they are collected on the same PC. These files are:

## `accelerometer-log.csv`

Results from the accelerometer in the format:

```
timestamp, aX, aY, aZ
```

* `timestamp` -- Floating point milliseconds since
epoch.

* `aX`, `aY`, `aZ` -- The accelerations, which are raw integer values
from the ADXL 345 chip. The X axis is positive towards the front of
the airplane; the Y axis is positive towards the left, and the Z axis
is positive towards the top of the plane.

## `telemetry-log.csv`

Results from the airdata probe in the format:

```
timestamp, rssi, seq, baro, temperature, dp0, dpA, dpB
```

* `timestamp` -- Floating point seconds since epoch.

* `rssi` -- RSSI value of radio reception quality.

* `seq` -- Internal sequence number.

* `baro` -- Barometric pressure in Pascals.

* `temperature` -- Ambient temperature in degrees Celsius.

* `dp0`, `dpA`, `dpB` -- Delta pressures from the probe nose in
  Pascals.

# Accelerometer calibration

We calibrated the accelerometer as described by SparkFun at

  https://learn.sparkfun.com/tutorials/adxl345-hookup-guide/all

and the result (for X, Y, and Z, respectively), is:

```
Accel Minimums: -257  -249  -264
Accel Maximums: 261  271  234
```

For any one axis, we define:

```
offset = 0.5 * (max + min)
gain = 0.5 * (max - min)

calibrated_value[i] = (raw_value[i] - offset) / gain
```


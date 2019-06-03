# Introduction

This data was from a flight test from KRHV to C83 and back again. The data logging PC ran
out of battery a while after takeoff from C83, which marked the end of the data stream.

Altimeter at KRHV at departure was 29.77 in Hg.

The telemetry was acquired from an Airball probe with 30 in. Hg All Sensors DLHR pressure
sensors.

The acceleration was acquired from a sensitive 3-axis accelerometer mounted on the aircraft
glareshield, sampling at 20 Hz.

The purpose was to correlate acceleration and airflow direction, especially in the yaw
direction, and determine if we should be using acceleration (scaled to dynamic pressure)
or direct yaw measurement for the yaw display in Airball.

# Analysis

We can see from the data that the telemetry signal is "lagging" behind the acceleration
signal by a large fraction of a second. This is likely a result of delays in the wireless
transmission path.

This means we cannot correlate the two data streams and therefore, unfortunately, means
we will need to re-do this experiment after we have solved the time lag problem.

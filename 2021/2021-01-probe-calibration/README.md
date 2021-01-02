This data was acquired with an [Airball probe
v8](http://www.airball.aero/2020/10/airball-probe-v8-mechanical-build.html)
on a boom mounted on a car on Hwy 101. There was a bunch of traffic,
so the data quiality is very poor, but it's what we were able to
acquire at the time.

We acquired data under cruise control, using "speedometer" phone app
that uses GPS to estimate true ground speed to determine the car's
speed in miles per hour. We ignored the effects of wind. We ran a
"zeroing" procedure to find the point in our altazimuth mounting for
the probe representing zero alpha and beta, saved that in a JSON file,
and moved the mount relative to that.

The goal was to determine a reasonable scaling factor between
theoretical "calibration" and actual observed data. This was not an
attempt to get an actual, accurate calibration.

We compare the values of `dp0/q`, `dpA/q` and `dpB/q` to the
theory. Then we proceed based on the hypothesis that theory and data
differ by a constant scaling factor, and plot the effect of that
scaling factor on the sums of the squares of the errors. We conclude
that we can get the best fit to the data when:

* We multiply theoretically predicted `dp0/q` by `0.5`
* We multiply theoretically predicted `dpA/q` and `dpB/q` by `0.7`

Clearly, this is very "dirty" data. We should repeat our experiments
with cleaner conditions when possible. But for now, we have some
scaling factors that we hope should give us more realistic results.
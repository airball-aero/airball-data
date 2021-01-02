#!/usr/bin/python

import sys

sys.path.append('/home/ihab/dynamixel_hr')

import experimentalfixture
import probetest

name = sys.argv[1]
mph = int(sys.argv[2])
alpha_beta = [int(sys.argv[3]), int(sys.argv[4])]

print('Acquiring "%s", %d mph, alpha_beta = %s' % (name, mph, alpha_beta))

t = probetest.ProbeTest(experimentalfixture.ExperimentalFixture())
t.acquire_point(name, mph, alpha_beta)

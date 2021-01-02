from probefixture import ProbeFixture

import random

class MockFixture(ProbeFixture):

    def __init__(self):
        self.az_el = [0.0, 0.0]
        self.mph = 0
        self.seq = 0
        
    def moveto(self, az_el):
        if az_el[0] > 45: az_el[0] = 45
        if az_el[1] > 45: az_el[1] = 45
        self.az_el = az_el

    def set_mph(self, mph):
        self.mph = int(mph)
        
    def read(self, n):
        q = self.q()
        dpA = (float(self.az_el[1]) / 45.0) * q + 15
        dpB = (float(self.az_el[0]) / 45.0) * q + 15
        dp0 = q - dpA - dpB
        oat = 25.0
        baro = 101325.0
        data = []
        for i in range(0, n):
            s = '$A,%d,%f,%f,%f,%f,%f' % (
                self.seq,
                self.noise(baro),
                self.noise(oat),
                self.noise(dp0),
                self.noise(dpA),
                self.noise(dpB),
            )
            data.append(s)
            self.seq = self.seq + 1
        self.seq = self.seq + int(random.uniform(1000, 2000))
        return data
            
    def q(self):
        return 0.5 * 1.225 * ((self.mph * 0.44704) ** 2)

    def noise(self, value):
        return value + random.uniform(-1.0, 1.0) * value * 0.05

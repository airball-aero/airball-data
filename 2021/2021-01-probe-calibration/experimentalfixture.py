from probefixture import ProbeFixture

import random
from dxl import *
from dxl.dxlcore import *
import time
import socket

class ExperimentalFixture(ProbeFixture):

    __az_id = 1
    __el_id = 2
    __speed = 50
    
    def __init__(self):
        self.__az_el = [0.0, 0.0]
        self.__seq = 0
        self.__chain = dxlchain.DxlChain('/dev/ttyACM0', rate=1000000)
        self.__chain.get_motor_list()
        
    def moveto(self, az_el):
        print('moveto(%s)' % (az_el))
        self.__az_el = [self.angle_limits(az_el[0]), self.angle_limits(az_el[1])]
        self.__chain.goto(
            self.__az_id,
            self.count(self.__az_el[0]),
            speed=self.__speed)
        self.__chain.goto(
            self.__el_id,
            self.count(self.__az_el[1]),
            speed=self.__speed)

    def read(self, n):
        print('read(%s)' % (n))
        r = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.4.1', 80))
        f = s.makefile()
        for i in range(0, n):
            while True:
                s = f.readline().strip()
                fields = s.split(',')
                if len(fields) > 0 and fields[0] == '$A':
                    print(s)
                    r.append(s)
                    break
        return r
            
    def count(self, degrees):
        count = int(float(degrees) / 0.29) + 512
        count = max(0, count)
        count = min(1023, count)
        return count
        
    def angle_limits(self, degrees):
        degrees = max(degrees, -45)
        degrees = min(degrees, 45)
        return degrees

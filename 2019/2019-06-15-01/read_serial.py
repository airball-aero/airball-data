#!/usr/bin/python

import serial
import io
import time

ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=100)

buf = ''

while True:
    for c in ser.read():
        if c == '\r' or c == '\n':
            if len(buf) > 0:
                print(('%f' % (time.time() * 1000)) + ',' + buf)
            buf = ''
        else:
            buf += c

ser.close()

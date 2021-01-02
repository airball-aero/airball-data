#!/usr/bin/python

import socket
import sys

alpha_total = 0.0
beta_total = 0.0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.4.1', 80))
f = s.makefile()

def match(prefix):
    if len(sys.argv) < 2:
        return True
    if sys.argv[1].lower() == prefix.lower():
        return True
    if ('$' + sys.argv[1].lower()) == prefix.lower():
        return True

while True:
    s = f.readline().strip()
    fields = s.split(',')
    if len(fields) > 0:
        if match(fields[0]):
            print(fields)

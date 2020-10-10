import socket
import string
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.4.1', 80))
f = s.makefile()

of = open('data.csv', 'a')

while True:
    line = string.strip(f.readline())
    print(line)
    if line.find('$B') == 0:
        of.write(str(time.time()))
        of.write(",")
        of.write(line)
        of.write("\n")
        of.flush()


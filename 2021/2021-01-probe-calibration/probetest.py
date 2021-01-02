import alphabeta
import numpy
import scipy.optimize as spo
import json
import os.path
import csv

class ProbeTest:

    __identity = lambda x: x
    
    __schema = [
        [ 'type', __identity ],
        [ 'seq', int ],
        [ 'baro', float ],
        [ 'oat', float ],
        [ 'dp0', float ],
        [ 'dpA', float ],
        [ 'dpB', float ],
    ]

    __statefile = 'state.json'

    __numsamples = 100

    __sweep_step = 5
    __sweep_count = 7
    
    def __init__(self, fixture):
        self.__fixture = fixture
        self.__zero = [0.0, 0.0]
        self.__load()
        print('self.__zero = %s' % (self.__zero))

    def __load(self):
        if not os.path.isfile(self.__statefile):
            return
        with open(self.__statefile) as f:
            x = json.load(f)
            self.__zero = x['zero']

    def __save(self):
        with open(self.__statefile, 'w') as f: 
            json.dump({'zero': self.__zero}, f)
        
    def find_zero(self):
        zero = self.__zero
        interval = 32
        for i in range(0, 6):
            zero = self.__estimate_zero(zero, interval)
            interval = interval / 2.0
        self.__zero = zero
        self.__save()

    def sweep(self, name, mph):
        name = str(name)
        mph = int(mph)
        for ai in range(-self.__sweep_count, self.__sweep_count + 1):
            for bi in range(-self.__sweep_count, self.__sweep_count + 1):
                alpha_beta = [
                    ai * self.__sweep_step,
                    bi * self.__sweep_step,
                ]
                self.acquire_point(name, mph, alpha_beta)

    def acquire_point(self, name, mph, alpha_beta):
        while True:
            az_el = alphabeta.alpha_beta_to_az_el(alpha_beta)
            az_el = [
                az_el[0] + self.__zero[0],
                az_el[1] + self.__zero[1],
            ]
            print('Acquiring: \"%s\" (%s mph), alpha_beta=%s az_el=%s' % (name, mph, alpha_beta, az_el))
            self.__fixture.moveto(az_el)
            lines = self.__fixture.read(self.__numsamples)
            print('Acquired %s lines, save (y)?' % (len(lines)))
            if input().strip().lower() == 'y':
                v = self.__csv_to_dict(lines)
                v['alpha'] = numpy.repeat(alpha_beta[0], len(v['baro']))
                v['beta'] = numpy.repeat(alpha_beta[1], len(v['baro']))
                v['mph'] = numpy.repeat(mph, len(v['baro']))        
                self.__save_csv(name, v)
                return

    def __save_csv(self, filename, column_dict):
        n = len(column_dict['baro'])
        full_filename = filename + '.csv'
        exists = os.path.isfile(full_filename)
        with open(full_filename, 'a+') as f:
            fieldnames = ['mph', 'alpha', 'beta', 'seq', 'baro', 'oat', 'dp0', 'dpA', 'dpB']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not exists: writer.writeheader()
            for i in range(0, n):
                row = {}
                for k in fieldnames: row[k] = str(column_dict[k][i])
                writer.writerow(row)
        
    def __estimate_zero(self, zero, interval):
        zero = self.__estimate_zero_az(zero, interval)
        zero = self.__estimate_zero_el(zero, interval)
        return zero

    def __estimate_zero_az(self, zero, interval):
        xl = [zero[0] - interval, zero[1]]
        xr = [zero[0] + interval, zero[1]]
        self.__fixture.moveto(xl)
        yl = self.__read_averaged(self.__numsamples)
        self.__fixture.moveto(xr)
        yr = self.__read_averaged(self.__numsamples)
        return [self.__line_root(xl[0], yl['dpB'], xr[0], yr['dpB']), zero[1]]

    def __estimate_zero_el(self, zero, interval):
        xd = [zero[0], zero[1] - interval]
        xu = [zero[0], zero[1] + interval]
        self.__fixture.moveto(xd)
        yd = self.__read_averaged(self.__numsamples)
        self.__fixture.moveto(xu)
        yu = self.__read_averaged(self.__numsamples)
        return [zero[0], self.__line_root(xd[1], yd['dpA'], xu[1], yu['dpA'])]
        
    def __read_averaged(self, n):
        while True:
            print('Read averaged?')
            if input().strip().lower() == 'y':
                break
        while True:
            v = self.__csv_to_dict(self.__fixture.read(n))
            r = {}
            for x in ['baro', 'oat', 'dp0', 'dpA', 'dpB']:
                r[x] = numpy.mean(v[x])
            print('Accept and continue?')
            if input().strip().lower() == 'y':            
                return r

    def __csv_to_dict(self, lines):
        r = {}
        for k in self.__schema:
            r[k[0]] = []
        for l in lines:
            a = l.split(',')
            for i in range(0, len(self.__schema)):
                r[self.__schema[i][0]].append(self.__schema[i][1](a[i]))
        return r

    def __line_root(self, x0, y0, x1, y1):
        return x0 + (0.0 - y0) / (y1 - y0) * (x1 - x0)

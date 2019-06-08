#!/usr/bin/python

import json
import numpy

def pressure_count_to_value_dlhr(count, fss, is_gage):
    os_dig = (0.1 if is_gage else 0.5) * pow(2, 24)
    total_range = fss if is_gage else 2.0 * fss
    return 1.25 * (count - os_dig) / pow(2, 24) * total_range

def pressure_count_to_value_hsc(count, fss, is_gage):
    p_min = 0 if is_gage else -fss
    p_max = fss
    n_ratio = (count * 1.0) / (pow(2, 14) * 1.0)
    return p_min + 1.25 * (n_ratio - 0.1) * (p_max - p_min)

def match_type(stype, req):
    return stype.lower().find(req) == 0

def pressure_count_to_value(count, stype, fss, is_gage):
    if match_type(stype, 'dlhr'):
        return pressure_count_to_value_dlhr(count, fss, is_gage)
    if match_type(stype, 'hsc'):
        return pressure_count_to_value_hsc(count, fss, is_gage)
    raise Exception('Sensor type unknown: %s' % stype)

def percent_full_scale(value, fss, is_gage):
    total_range = fss if is_gage else 2.0 * fss
    return value / total_range * 100

water_density_by_temp = [
    [ 0.0, 4.4, 10.0, 15.6, 21.1, 26.7, 32.2 ],
    [ 1.0031, 1.0031, 1.0031, 1.0024, 1.0012, 0.9999, 0.9981 ]
]

def correct_value_for_density(water_column_height, temperature):
    d0 = numpy.interp(4.0, water_density_by_temp[0], water_density_by_temp[1])
    d1 = numpy.interp(temperature, water_density_by_temp[0], water_density_by_temp[1])
    return water_column_height * d1 / d0

def process_measurement(is_gage, fss, temp, stype, values):
    vmin = pressure_count_to_value(values['cmin'], stype, fss, is_gage)
    vavg = pressure_count_to_value(values['cavg'], stype, fss, is_gage)
    vmax = pressure_count_to_value(values['cmax'], stype, fss, is_gage)

    pct_delta_min = percent_full_scale(vmin - vavg, fss, is_gage)
    pct_delta_max = percent_full_scale(vmax - vavg, fss, is_gage)

    applied = correct_value_for_density(values['applied'], temp)

    pct_err_avg = percent_full_scale(vavg - applied, fss, is_gage)

    print('%+ 7.3f inH2O => %+ 7.3f inH2O, min=%+ 7.3f %%fs, max=%+ 7.3f %%fs, err=%+ 8.3f %%fs' %
          (applied, vavg, pct_delta_min, pct_delta_max, pct_err_avg))
    
def process_sensor(data):
    notes = (" [%s]" % data['notes']) if data.has_key('notes') else ""
    print('%s (%s)%s' % (data['type'], data['id'], notes))
    for m in data['measurements']:
        process_measurement(data['gage'], data['fss'], data['temp'], data['type'], m)

with open('data.json') as f:
    data = json.load(f)

for sensor in data:
    process_sensor(sensor)

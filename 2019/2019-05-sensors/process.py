#!/usr/bin/python

import json

def pressure_count_to_value(count, fss, is_gage):
    os_dig = (0.1 if is_gage else 0.5) * pow(2, 24)
    total_range = fss if is_gage else 2.0 * fss
    return 1.25 * (count - os_dig) / pow(2, 24) * total_range

def percent_full_scale(value, fss, is_gage):
    total_range = fss if is_gage else 2.0 * fss
    return value / total_range * 100

def process_measurement(is_gage, fss, temp, values):
    vmin = pressure_count_to_value(values['cmin'], fss, is_gage)
    vavg = pressure_count_to_value(values['cavg'], fss, is_gage)
    vmax = pressure_count_to_value(values['cmax'], fss, is_gage)

    pct_delta_min = percent_full_scale(vmin - vavg, fss, is_gage)
    pct_delta_max = percent_full_scale(vmax - vavg, fss, is_gage)

    pct_err_avg = percent_full_scale(vavg - values['applied'], fss, is_gage)

    print('%+ 5.1f inH2O => %+ 7.3f inH2O, min=%+ 7.3f %%fs, max=%+ 7.3f %%fs, err=%+ 8.3f %%fs' %
          (values['applied'], vavg, pct_delta_min, pct_delta_max, pct_err_avg))
    
def process_sensor(data):
    notes = (" [%s]" % data['notes']) if data.has_key('notes') else ""
    print('%s (%s)%s' % (data['type'], data['id'], notes))
    for m in data['measurements']:
        process_measurement(data['gage'], data['fss'], data['temp'], m)

with open('data.json') as f:
    data = json.load(f)

for sensor in data:
    process_sensor(sensor)

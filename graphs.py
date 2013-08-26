#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import csv
from datetime import datetime
import os
import os.path

reader = csv.DictReader(open('generation_demand_full.csv', 'r'))



if not os.path.exists('graph_data'):
  os.mkdir('graph_data')

daily_data = {}
monthly_data = {}

for row in reader:
  timestamp = datetime.strptime(row['timestamp'].replace('A', '').replace('B', ''), '%Y-%m-%d %H:%M')
  del row['timestamp']
  date = timestamp.date()
  month = timestamp.strftime('%Y%m')
  if date not in daily_data:
    daily_data[date] = dict([(key, []) for key in row.keys()])
  if month not in monthly_data:
    monthly_data[month] = dict([(key, []) for key in row.keys()])
  for key, value in row.items():
    if len(value.strip()) == 0:
      print 'WARNING: Empty value for "%s" in %s' % (key, str(timestamp))
      value = 0
    daily_data[date][key].append(int(value))
    monthly_data[month][key].append(int(value))


files = {}
for field in daily_data.values()[0]:
  files[field] = open('graph_data/full_daily_%s.dat' % field, 'w')
  files[field + '_pct'] = open('graph_data/full_daily_pct_%s.dat' % field, 'w')
  files[field + '_monthly'] = open('graph_data/full_monthly_%s.dat' % field, 'w')
  files[field + '_monthly_pct'] = open('graph_data/full_monthly_pct_%s.dat' % field, 'w')

for date, data_dict in sorted(daily_data.items(), key=lambda x: x[0]):
  for field in data_dict.keys():
    data_dict[field] = sum(data_dict[field])
    files[field].write('%s\t%f\n' % (date.strftime('%Y%m%d'), data_dict[field]))
  demand = float(data_dict['demand'])
  for field in data_dict.keys():
    files[field + '_pct'].write('%s\t%f\n' % (date.strftime('%Y%m%d'), data_dict[field] / demand))

for month, data_dict in sorted(monthly_data.items(), key=lambda x: x[0]):
  for field in data_dict.keys():
    data_dict[field] = sum(data_dict[field])
    files[field + '_monthly'].write('%s\t%f\n' % (month, data_dict[field]))
  demand = float(data_dict['demand'])
  for field in data_dict.keys():
    files[field + '_monthly_pct'].write('%s\t%f\n' % (month, data_dict[field] / demand))

for fs in files.values():
  fs.close()

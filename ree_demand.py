#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ree_demanda.py
#
# Copyright © 2013 Santiago M. Mola <santi@mola.io>
#   Licensed under the MIT License.
#
# https://github.com/smola/ree-demanda
#

import logging

logging.basicConfig(level=logging.INFO)

from suds.client import Client

#logging.getLogger('suds.client').setLevel(logging.DEBUG)

DEMANDA_30_SERVICE_WSDL_URL = 'https://demanda.ree.es/WSVisionaV01/wsDemanda30Service?WSDL'
DEMANDA_30_FINO_SERVICE_WSDL_URL = 'https://demanda.ree.es/WSVisionaV01/wsDemanda30FinoService?WSDL'

class REE(object):

  def __init__(self):
    self._client = Client(DEMANDA_30_SERVICE_WSDL_URL)
    self._clientFino = Client(DEMANDA_30_FINO_SERVICE_WSDL_URL)

  def time_query(self):
    return self._clientFino.service.consultaTiempo()

  def _update_key(self):
    """
    Generates a timestamp-based key expected by the server.
    """
    t = self.time_query()
    self._clave = str(int(float(t[5:10])/ 1.307000))

  def _transform_forecast_programmed_response(self, response):
    result = []
    for previstaProgramada in response.valoresPrevistaProgramada:
      result.append({
        'programmed': previstaProgramada.programada,
        'forecast': previstaProgramada.prevista,
        'timestamp': previstaProgramada.timeStamp
      })
    return result

  def forecast_programmed(self, fecha):
    self._update_key()
    return self._transform_forecast_programmed_response(
      self._clientFino.service.prevProgFino(fecha, self._clave)
    )

  def _transform_min_max_values_response(self, response):
    return {
      'min': response.min,
      'max': response.max,
      'timestamp_min': response.timeStampMin,
      'timestamp_max': response.timeStampMax
    }

  def min_max_values(self, fecha):
    self._update_key()
    return self._transform_min_max_values_response(
      self._clientFino.service.valoresMaxMinFino(fecha, self._clave)
    )

  def _transform_generation_demand_response(self, response):
    result = []
    for generacionComponentesFino in response.valoresHorariosGeneracion:
      result.append({
        'autoproduction': generacionComponentesFino.autoprod,
        'coal': generacionComponentesFino.carbon,
        'combined_cycle': generacionComponentesFino.cicloComb,
        'eolic': generacionComponentesFino.eolica,
        'fuel_gas': generacionComponentesFino.gasFuel,
        'hydroelectric': generacionComponentesFino.hidro,
        'international_exchange': generacionComponentesFino.intercambios,
        'balearic_link': generacionComponentesFino.intercambiosCableBal,
        'nuclear': generacionComponentesFino.nuclear,
        'solar': generacionComponentesFino.solar,
        'demand': generacionComponentesFino.demanda,
        'timestamp': generacionComponentesFino.timeStamp
      })
    return result

  def generation_demand(self, fecha):
    self._update_key()
    return self._transform_generation_demand_response(
      self._client.service.demandaGeneracion30(fecha, self._clave)
    )

if __name__ == '__main__':
  r = REE()
  from datetime import datetime
  from calendar import Calendar
  from itertools import chain
  import json
  import os
  import os.path
  import csv

  if not os.path.exists('data'):
    os.mkdir('data')

  generationDemandWriter = csv.DictWriter(open('generation_demand_full.csv', 'w'), ['timestamp', 'demand', 'forecast', 'programmed', 'nuclear', 'coal', 'fuel_gas', 'combined_cycle', 'hydroelectric', 'solar', 'eolic', 'autoproduction', 'balearic_link', 'international_exchange'])
  generationDemandWriter.writeheader()

  all_data = {}

  now = datetime.now()
  calendar = Calendar()

  for year in range(2007, now.year + 1):
    for date in filter(lambda x: x.year == year, chain(*chain(*calendar.yeardatescalendar(year, 12)[0]))):
      if datetime(date.year, date.month, date.day) > now:
        break
      d = date.strftime('%Y-%m-%d')

      filename = 'data/generation_demand_%s.json' % d
      if not os.path.exists(filename):
        data = r.generation_demand(d)
        json.dump(data, open(filename, 'w'))
      else:
        data = json.load(open(filename, 'r'))
      for datum in data:
        if datum['timestamp'] not in all_data:
          all_data[datum['timestamp']] = datum

      filename = 'data/forecast_programmed_%s.json' % d
      if not os.path.exists(filename):
        data = r.forecast_programmed(d)
        json.dump(data, open(filename, 'w'))
      else:
        data = json.load(open(filename, 'r'))
      for datum in data:
        if datum['timestamp'] in all_data:
          all_data[datum['timestamp']]['forecast'] = datum['forecast']
          all_data[datum['timestamp']]['programmed'] = datum['programmed']

  for timestamp in sorted(all_data.keys(), key=lambda key: datetime.strptime(key.replace('A', '').replace('B', ''), '%Y-%m-%d %H:%M')):
    generationDemandWriter.writerow(all_data[timestamp])

import requests
import json
import os


class Weather:
  DARK_SKY_BASE_URL = 'https://api.darksky.net/forecast'
  STATUS_RAIN = ['rain', 'snow', 'sleet']

  def __init__(self):
    self.dark_sky_api_key = os.environ['DARK_SKY_API_KEY']

  def set_geo(self, **kwargs):
    self.lat = kwargs['lat']
    self.lon = kwargs['lon']

  def is_it_rains(self):
    response_today = self._get_response_today()
    status = self._get_status(response_today)

    return 'precipType' in response_today

  def _get_response_today(self):
    uri = '{0}/{1}/{2},{3}'.format(
        self.DARK_SKY_BASE_URL, self.dark_sky_api_key,
        self.lat, self.lon
    )
    return requests.get(uri).json()['daily']['data'][0]

  def _get_status(self, response):
    return response['icon']


def lambda_function(event={}, context={}):
  weather = Weather()
  weather.set_geo(lat=35.7004, lon=139.805)
  print(weather.is_it_rains())

  return 0

if __name__ == '__main__':
  lambda_function()



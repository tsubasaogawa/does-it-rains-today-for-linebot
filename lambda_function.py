import requests
import json
import os
import linebot_publisher


class Weather:
  DARK_SKY_BASE_URL = 'https://api.darksky.net/forecast'
  STATUS_RAIN = ['rain', 'snow', 'sleet']

  def __init__(self):
    self.dark_sky_api_key = os.environ['DARK_SKY_API_KEY']

  def set_geo(self, **kwargs):
    self.lat = kwargs['lat']
    self.lon = kwargs['lon']

  def get_precip_probability(self):
    response_today = self._get_response_today()
    # status = self._get_status(response_today)

    if not 'precipType' in response_today:
      return 0

    return round(response_today['precipProbability'] * 100)

  def _get_response_today(self):
    uri = '{0}/{1}/{2},{3}'.format(
        self.DARK_SKY_BASE_URL, self.dark_sky_api_key,
        self.lat, self.lon
    )
    return requests.get(uri).json()['daily']['data'][0]

  def _get_status(self, response):
    return response['icon']


def lambda_handler(event={}, context={}):
  weather = Weather()
  publisher = linebot_publisher.LineBotPublisher()
  weather.set_geo(lat=35.7004, lon=139.805)
  prob = weather.get_precip_probability()
  if prob > 0 and os.environ['CAN_POST_TO_LINE']:
    publisher.post_text(
      os.environ['LINE_BOT_TO_ID'],
      '今日は雨が降りそう (降水確率: {0}%)'.format(prob)
    )

  return 0

if __name__ == '__main__':
  lambda_handler()


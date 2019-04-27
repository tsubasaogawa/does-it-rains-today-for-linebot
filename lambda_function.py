import requests
import json
import os
import pytz
from datetime import datetime
import linebot_publisher


class Weather:
  DARK_SKY_BASE_URL = 'https://api.darksky.net/forecast'
  STATUS_RAIN = ['rain', 'snow', 'sleet']

  def __init__(self):
    self.dark_sky_api_key = os.environ['DARK_SKY_API_KEY']
    tz = pytz.timezone('Asia/Tokyo')
    today_12am = int(datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%s'))
    self.tomorrow_12am = today_12am + 86400

  def set_geo(self, **kwargs):
    self.lat = kwargs['lat']
    self.lon = kwargs['lon']

  def get_max_precip_probability(self):
    precip_probs = self._get_precip_probabilities()
    if not precip_probs:
      return 0

    print('Obtained probabilities: {0}'.format(precip_probs))

    max_precip_prob = max(precip_probs)
    # status = self._get_status(response_today)

    return round(max_precip_prob * 100)

  def _get_precip_probabilities(self):
    uri = '{0}/{1}/{2},{3}'.format(
        self.DARK_SKY_BASE_URL, self.dark_sky_api_key,
        self.lat, self.lon
    )
    responses = requests.get(uri).json()['hourly']['data']

    precip_probs = []
    for i, response in enumerate(responses):
      if response['time'] >= self.tomorrow_12am:
        break
      elif 'precipType' not in response:
        continue
      precip_probs.append(response['precipProbability'])

    print(precip_probs)
    return precip_probs

  def _get_status(self, response):
    return response['icon']


def lambda_handler(event={}, context={}):
  weather = Weather()
  publisher = linebot_publisher.LineBotPublisher()
  weather.set_geo(lat=35.7004, lon=139.805)
  prob = weather.get_max_precip_probability()
  print("Today's max precip probability is {0}%".format(prob))
  if prob > int(os.environ['PRECIP_THRESHOLD_PERCENT']) and os.environ['CAN_POST_TO_LINE']:
    publisher.post_text(
      os.environ['LINE_BOT_TO_ID'],
      '今日は雨が降りそう (降水確率: {0}%)'.format(prob)
    )

  return 0

if __name__ == '__main__':
  lambda_handler()


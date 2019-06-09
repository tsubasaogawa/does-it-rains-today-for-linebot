import requests
import os
import pytz
import sys
from datetime import datetime
# https://github.com/tsubasaogawa/linebot-publisher-layer
import linebot_publisher


class Weather:
    DARK_SKY_BASE_URL = 'https://api.darksky.net/forecast'

    def __init__(self):
        """
        Constructor.
        """
        self.dark_sky_api_key = os.environ.get('DARK_SKY_API_KEY')

        # Set target range
        tz = pytz.timezone('Asia/Tokyo')
        today_12am = int(datetime.now(tz).replace(
            hour=0, minute=0, second=0, microsecond=0).strftime('%s'))
        self.tomorrow_12am = today_12am + 86400

    def set_geo(self, **kwargs):
        """
        Set latitude and longitude.

        Parameters
        ----------
        lat (keyword): double
            Latitude.
        lon (keyword): double
            Longitude.
        """
        self.lat = kwargs['lat']
        self.lon = kwargs['lon']

    def get_max_precip_probability(self):
        """
        Get the max probability of precipitation today.

        Returns
        -------
        max_precip_percent : int
            Max probability of precipitation (%)
        """
        precip_probs = self._get_precip_probabilities()
        if not precip_probs:
            return 0

        print('Obtained probabilities: {0}'.format(precip_probs))

        max_precip_prob = max(precip_probs)
        # status = self._get_status(response_today)

        return round(max_precip_prob * 100)

    def _get_precip_probabilities(self):
        """
        Get probabilities of precipitation per an hour.
        It calls the dark sky api.

        Returns
        -------
        precip_probs : list[double]
            Probabilities of precipitation.
        """
        uri = '{0}/{1}/{2},{3}'.format(
            self.DARK_SKY_BASE_URL,
            self.dark_sky_api_key,
            self.lat, self.lon
        )
        # Hourly
        responses = requests.get(uri).json()['hourly']['data']

        precip_probs = []
        for i, response in enumerate(responses):
            # exceeds
            if response['time'] >= self.tomorrow_12am:
                break
            # it does not rain
            elif 'precipType' not in response:
                continue

            precip_probs.append(response['precipProbability'])

        print(precip_probs)
        return precip_probs

    def _get_status(self, response):
        """
        Get a simple weather status.

        Parameters
        ----------
        response : dict
            Response['hourly']['data'] from dark sky api.

        Returns
        -------
        status : string
            Weather status.
        """
        return response['icon']


def lambda_handler(event={}, context={}):
    """
    Lambda handler.

    Returns
    -------
    result : int
        0.
    """
    weather = Weather()
    publisher = linebot_publisher.LineBotPublisher()
    weather.set_geo(**get_geo())

    prob = weather.get_max_precip_probability()
    print("Today's max precip probability is {0}%".format(prob))

    threshold = os.environ.get('PRECIP_THRESHOLD_PERCENT')
    if not threshold:
        threshold = '30'

    if prob > int(threshold) and os.environ.get('CAN_POST_TO_LINE'):
        publisher.post_text(
            os.environ['LINE_BOT_TO_ID'],
            '今日は雨が降りそう (降水確率: {0}%)'.format(prob)
        )

    return 0


def get_geo():
    """
    Get latitude and longitude from environment variables.

    Returns
    -------
    geo : dict
        lat : double
            Latitude obtained from $WEATHER_LATITUDE.
        lon : double
            Longitude obtained from $WEATHER_LONGITUDE.
    """
    lat = os.environ.get('WEATHER_LATITUDE')
    lon = os.environ.get('WEATHER_LONGITUDE')
    if not lat or not lon:
        print('Please set environment variables of WEATHER_LATITUDE and WEATHER_LONGITUDE.')
        sys.exit(1)

    return {
        'lat': lat,
        'lon': lon,
    }


if __name__ == '__main__':
    lambda_handler()

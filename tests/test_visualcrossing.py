import pytest
import requests

from common.weather_api import VisualCrossing

# Reusable constants
LATITUDE = 51.5072
LONGITUDE = 0.1276
START_DATE = '2023-03-20'
DAYS_AHEAD = 1

device_data = {
    '_device_id': 1,
    'device_name': 'TEST RTMU',
    'prediction_status': 1,
    'latitude': 52.956240,
    'longitude': -1.184660,
    'model_id': 2,
    'depo_location': 'Nottingham'
}


class TestVisualCrossing:
    @pytest.fixture
    def visualcrossing(self):
        return VisualCrossing()

    def test_init(self, visualcrossing):
        assert visualcrossing.base_url == 'https://weather.visualcrossing.' \
            'com/VisualCrossingWebServices/rest/services/timeline/'

    def test_generate_api_url(self, visualcrossing):
        api_url = visualcrossing.generate_api_url(
            LATITUDE, LONGITUDE, START_DATE, DAYS_AHEAD
        )
        assert api_url == 'https://weather.visualcrossing.com/' \
            'VisualCrossingWebServices/rest/services/timeline/' \
            '51.5072,0.1276/2023-03-20/2023-03-21?&unitGroup=metric&' \
            'contentType=csv&include=hours&elements=' \
            'datetime,temp,dew,humidity,precip,visibility,solarradiation,' \
            'solarenergy&key=CX3DPJRU94QMC5WJ6R4V2X6UM'

    def test_api_url_status(self, visualcrossing):
        api_url = visualcrossing.generate_api_url(
            LATITUDE, LONGITUDE, START_DATE, DAYS_AHEAD
        )
        status_code = requests.get(api_url).status_code
        assert status_code == 200

    def test_add_manual_fields(self, visualcrossing):
        json_data = visualcrossing.fetch_api_data(
            LATITUDE, LONGITUDE, START_DATE, DAYS_AHEAD
        )
        data_df = visualcrossing.add_manual_fields(json_data, device_data)
        assert 'month' in list(data_df.columns)
        assert 'day_of_year' in list(data_df.columns)
        assert 'hour_of_day' in list(data_df.columns)

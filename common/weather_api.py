import pandas as pd
import requests

from common import utils
from common.sql import Devices, PredParams


class OpenMeteo:
    def __init__(self):
        self.base_url = 'https://api.open-meteo.com/v1/forecast?'
        open_meteo_params = PredParams().get_all_provider_parameters(
            'Open-Meteo')
        self.available_params = [
            p['parameter_name'] for p in open_meteo_params
        ]

    def generate_api_url(self, lat, lon, start_date, days_ahead):
        """Take a list of parameters and generate a full URL

        start-date must come in a format 'year-mm-dd'
        e.g. '2023-03-25'
        """
        # Format latitude and longitude
        lat_lon = f'latitude={lat}&longitude={lon}'

        # Format start and end date
        start, end = utils.calculate_time_ahead(start_date, days_ahead)
        start_end_dates = f'start_date={start}&end_date={end}'

        # Format params
        parameters = ','.join(self.available_params)

        api_url = f'{self.base_url}{lat_lon}&{start_end_dates}' \
                  f'&hourly={parameters}'

        return api_url

    def fetch_api_data(self, lat, lon, start_date, days_ahead):
        """Fetch api data and return it as a json"""
        api_url = self.generate_api_url(lat, lon, start_date, days_ahead)
        response = requests.get(api_url)
        return response.json()

    def add_manual_fields(self, json_data, device_data):
        # Convert to pandas df
        json_df = pd.DataFrame(json_data['hourly'])

        # Add time related features
        json_df['time'] = pd.to_datetime(json_df['time'])
        json_df['month'] = json_df['time'].dt.month
        json_df['day_of_year'] = json_df['time'].dt.day_of_year
        json_df['hour_of_day'] = json_df['time'].dt.hour
        json_df['azimuth'] = 0
        json_df['altitude'] = 0

        # Add depot
        json_df['depo_location'] = device_data['depo_location']
        json_df['depo_location'] = json_df['depo_location'].astype('category')

        return json_df

    def weather_pipe(self, device_id, start_date, days_ahead):
        # Get device data to extract latitude and longitude
        device_data = Devices().get_one(device_id)

        # Get json data from the API
        raw_json_data = self.fetch_api_data(
            device_data['latitude'], device_data['longitude'],
            start_date, days_ahead)

        # Process API data to include extra fields
        processed_data = self.add_manual_fields(raw_json_data, device_data)

        return processed_data

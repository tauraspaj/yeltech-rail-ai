import pandas as pd
import requests

from common import utils


class OpenMeteo:
    def __init__(self):
        self.base_url = 'https://api.open-meteo.com/v1/forecast?'
        # ToDo: Extract this list from the database
        self.available_params = [
            'temperature_2m',
            'relativehumidity_2m',
            'dewpoint_2m',
            'apparent_temperature',
            'precipitation',
            'cloudcover',
            'cloudcover_low',
            'cloudcover_mid',
            'cloudcover_high',
            'shortwave_radiation',
            'et0_fao_evapotranspiration',
            'windspeed_10m',
            'direct_radiation',
            'diffuse_radiation',
            'direct_normal_irradiance'
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

    def process_json_data(self, json_data):
        # Convert to pandas df
        json_df = pd.DataFrame(json_data['hourly'])

        # Add time related features
        json_df['time'] = pd.to_datetime(json_df['time'])
        json_df['month'] = json_df['time'].dt.month
        json_df['day_of_year'] = json_df['time'].dt.day_of_year
        json_df['hour_of_day'] = json_df['time'].dt.hour

        # Drop params that weren't used in the model
        proc_data = json_df.copy(deep=True)
        proc_data = proc_data.drop(columns=['time', 'precipitation'])

        return proc_data

    def weather_pipe(self, lat, lon, start_date, days_ahead):
        json_data = self.fetch_api_data(lat, lon, start_date, days_ahead)
        proc_data = self.process_json_data(json_data)
        return json_data, proc_data

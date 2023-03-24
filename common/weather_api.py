from datetime import date, timedelta

import pandas as pd
import requests


def get_weather_api(lat=52.95624, lon=-1.18466, days_ahead=7):

    # open-meteo
    base_url = r'https://api.open-meteo.com/v1/forecast?'

    lat = 'latitude=' + str(lat)
    lon = '&longitude=' + str(lon)
    start_date = '&start_date=' + str(date.today())
    end_date = '&end_date=' + str(date.today() + timedelta(days=days_ahead))
    params = '&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,' \
        'precipitation,rain,snowfall,cloudcover,cloudcover_low,' \
        'cloudcover_mid,cloudcover_high,shortwave_radiation,' \
        'direct_radiation, diffuse_radiation,direct_normal_irradiance,' \
        'windspeed_10m'

    total_url = base_url + lat + lon + start_date + end_date + params

    return total_url


def get_weather_data(total_url):

    response = requests.get(total_url)
    result = response.json()

    raw_weather = pd.DataFrame(result['hourly'])

    return raw_weather


def process_data(raw_weather):

    # add time related features
    raw_weather['time'] = pd.to_datetime(raw_weather['time'])
    raw_weather['month'] = raw_weather['time'].dt.month
    raw_weather['day_of_year'] = raw_weather['time'].dt.day_of_year
    raw_weather['hour_of_day'] = raw_weather['time'].dt.hour

    # drop params that weren't used in the model
    proc_weather = raw_weather.copy(deep=True)
    proc_weather = proc_weather.drop(columns=['time', 'precipitation'])

    return proc_weather


def weather_pipe():

    total_url = get_weather_api()
    raw_weather = get_weather_data(total_url)
    proc_weather = process_data(raw_weather)

    return raw_weather, proc_weather

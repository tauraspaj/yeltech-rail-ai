import json

import pandas as pd

from common.sql import Models, Devices
from common.utils import load_model
from common.weather_api import OpenMeteo


def prediction_pipeline(device_id, start_date, days_ahead):
    # Find model is used by device
    model_id = Devices().get_one(device_id)['model_id']

    # Retrieve the model
    model = load_model(model_id)

    # Get a list of params that the model was trained on
    model_params = Models().get_model_parameters(model_id)

    # Get raw data and append required fields. This will return pandas df
    all_data = OpenMeteo().weather_pipe(device_id, start_date, days_ahead)

    # Execute the prediction
    execute_prediction(model, all_data, model_params)


def execute_prediction(model, all_data, model_params):
    # Filter all_data to only params model was trained on
    filtered_df = all_data.filter(model_params)

    # Reorder the columns so they're acceptable by the model
    cols_when_model_builds = model.get_booster().feature_names
    filtered_df = filtered_df[cols_when_model_builds]

    # Get predictions
    predictions = model.predict(filtered_df)

    # Convert predictions array into a df
    df_predictions = pd.DataFrame(predictions, columns=['predicted_temp'])
    # Append a time to each prediction
    df_result = pd.concat([df_predictions, all_data[['time']]], axis=1)
    df_result['time'] = pd.DatetimeIndex(df_result['time'].values)

    # Generate device readings in an acceptable json format
    device_readings = []
    for i in df_result.iterrows():
        device_readings.append({
            'timestamp': i[1]['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'reading': json.dumps(eval(str(i[1]['predicted_temp'])))[:4]
        })

    return device_readings

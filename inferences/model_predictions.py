import json
from datetime import datetime

import pandas as pd

from common import logger
from common.sql import Devices, Models, save_predictions_to_db
from common.utils import load_model
from common.weather_api import OpenMeteo, VisualCrossing

log = logger.get_logger()


def prediction_pipeline(device_id, start_date, days_ahead):
    # Find model is used by device
    try:
        model_id = Devices().get_one(device_id)['model_id']
        # Retrieve the model
        model = load_model(model_id)
    except Exception as e:
        log.error(
            "[DiD: %d] Failed to load the model. Ending process. "
            "Error: %s", device_id, e)
        return

    # Get a list of params that the model was trained on
    try:
        model_params = Models().get_model_parameters(model_id)
    except Exception as e:
        log.error(
            "[DiD: %d] Failed to get model params. Ending process. "
            "Error: %s", device_id, e)
        return

    # Get raw data and append required fields. This will return pandas df
    try:
        all_data = VisualCrossing().weather_pipe(
            device_id, start_date, days_ahead
        )
    except Exception as e:
        log.error(
            "[DiD: %d] Failed to get weather data. Ending process. "
            "Error: %s", device_id, e)
        return

    # Get current time as time_of_execution
    time_of_execution = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Execute the prediction
    try:
        if not (predictions := execute_prediction(
                model, all_data, model_params)):
            return
    except Exception as e:
        log.error(
            "[DiD: %d] Failed to execute predictions. Ending process. "
            "Error: %s", device_id, e)
        return

    # Save predictions and data to the database
    try:
        save_predictions_to_db(
            predictions, all_data, time_of_execution, device_id)
    except Exception as e:
        log.error(
            "[DiD: %d] Failed to save predictions to database. "
            "Ending process. Error: %s", device_id, e)
        return

    return


def execute_prediction(model, all_data, model_params):
    # Filter all_data to only params model was trained on
    filtered_df = all_data.filter(model_params)

    # Reorder the columns so they're acceptable by the model
    try:
        cols_when_model_builds = model.get_booster().feature_names
    except AttributeError:
        try:
            cols_when_model_builds = model.feature_name_
        except Exception as e:
            log.error(
                "Unable to re-order columns to match the model. "
                "Ending process. Error: %s", e)
            return
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

# imports
import pandas as pd
import json
from ..common.ml_utils import load_model


def run_prediction(proc_weather, raw_weather):

    # 1) load model from models file
    model = load_model(
        'rtmu_2716_openmeteo_global_winter_model_V2.pkl'
    )

    # 2) make prediction
    preds = model.predict(proc_weather)

    df_preds = pd.DataFrame(preds, columns=['predicted_temp'])
    df_res = pd.concat([df_preds, raw_weather[['time']]], axis=1)
    df_res['time'] = pd.DatetimeIndex(df_res['time'].values)

    # need to make float32 json serializable
    device_readings = []
    for val in range(50):
        for i in df_res.iterrows():
            device_readings.append({
                'timestamp': i[1]['time'].strftime('%Y-%m-%d %H:%M:%S'),
                'reading': json.dumps(eval(str(i[1]['predicted_temp'])))[:4]
            })

    return device_readings

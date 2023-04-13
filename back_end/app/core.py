from common import weather_api
from inferences import model_predictions


def get_predictions():
    raw_weather, proc_weather = weather_api.weather_pipe()
    preds = model_predictions.run_prediction(proc_weather, raw_weather)

    return preds

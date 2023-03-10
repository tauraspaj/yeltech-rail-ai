import logging
import math

from .inferences.model_predictions import run_prediction
from .common.weather_api import weather_pipe

import config

logging.basicConfig(level=config.LOGLEVEL)
logger = logging.getLogger(__name__)


def get_predictions():

    raw_weather, proc_weather = weather_pipe()
    preds = run_prediction(proc_weather, raw_weather)

    return preds

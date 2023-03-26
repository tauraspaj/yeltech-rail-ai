import errno
import os.path
import pickle
from datetime import datetime, timedelta

from common.paths import MODELS_DIR
from common.sql import Models


def load_model(model_id):
    return fetch_model(Models().get_one(model_id)['model_file_name'])


def fetch_model(model_name):
    model_path = os.path.join(MODELS_DIR, model_name)

    # Check if path exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), model_path)

    model = pickle.load(open(model_path, 'rb'))
    return model


def calculate_time_ahead(start_date, days_ahead):
    start_date_object = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_object = start_date_object + timedelta(days=days_ahead)
    return str(start_date_object), str(end_date_object)

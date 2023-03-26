import errno
import os.path
import pickle
from datetime import datetime, timedelta

from .paths import ROOT_DIR


def load_model(model_name):
    model_path = os.path.join(ROOT_DIR, 'assets/models', model_name)

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

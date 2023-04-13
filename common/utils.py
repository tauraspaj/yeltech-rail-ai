import errno
import os.path
import pickle
from datetime import datetime, timedelta

from common import sql
from common.paths import MODELS_DIR


def load_model(model_id):
    return fetch_model(sql.Models().get_one(model_id)['model_file_name'])


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


def convert_model_param_list_to_dict(params):
    id_to_param_dict = {}
    for param in params:
        id_to_param_dict[param['parameter_name']] = param['_parameter_id']
    return id_to_param_dict

import os.path
import pickle
import errno

from .paths import ROOT_DIR


def load_model(model_name):
    model_path = os.path.join(ROOT_DIR, 'assets/models', model_name)

    # Check if path exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), model_path)

    model = pickle.load(open(model_path, 'rb'))
    return model

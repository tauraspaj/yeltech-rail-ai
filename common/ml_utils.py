import pickle
import os.path
from ..paths import ROOT_DIR


def load_model(model_name):
    model_path = os.path.join(ROOT_DIR, 'assets/models', model_name)
    model = pickle.load(open(model_path, 'rb'))
    return model

from app import core


def say_hello():
    return {"message": "Hello API!"}


def run_predictions():
    return core.get_predictions()

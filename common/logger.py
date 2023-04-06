import logging
import os

from common import paths


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
    )

    path_to_logs = os.path.join(paths.ROOT_DIR, 'logs')
    if not os.path.exists(path_to_logs):
        os.makedirs(path_to_logs)

    file_handler = logging.FileHandler(
        os.path.join(path_to_logs, 'history.log'),
        mode='a'
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

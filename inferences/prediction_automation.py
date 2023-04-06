from datetime import date

from common import logger
from common.sql import Devices
from inferences.model_predictions import prediction_pipeline

logger = logger.setup_logger()


# Fetch all device ids from the database
device_ids = Devices().get_all()

start_date = date.today()

for device in device_ids:
    logger.info('|===== [DiD: %d] Starting prediction pipeline =====|',
                device['_device_id'])

    if device['prediction_status'] == 0:
        logger.info('[DiD: %d]}] Prediction status 0. Skipping..',
                    device['_device_id'])
        continue

    prediction_pipeline(device['_device_id'], str(start_date), days_ahead=6)
    logger.info('[DiD: %d] Prediction pipeline finished!',
                device['_device_id'])

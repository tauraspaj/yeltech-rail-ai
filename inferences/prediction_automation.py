import sys
from datetime import date

from common import logger
from common.sql import Devices
from inferences.model_predictions import prediction_pipeline

log = logger.get_logger()

log.info("====================== PREDICTION AUTOMATION ======================")

# Fetch all device ids from the database
try:
    device_ids = Devices().get_all()
except Exception as e:
    log.error(
        "Problem fetching device ids. "
        "Ending process. Error: %s", e)
    sys.exit()

# Fetch todays date
start_date = date.today()

for device in device_ids:
    log.info('------ [DiD: %d] Starting prediction pipeline ------',
             device['_device_id'])

    if device['prediction_status'] == 0:
        log.warning('[DiD: %d]}] Prediction status 0. Skipping...',
                    device['_device_id'])
        continue

    prediction_pipeline(device['_device_id'], str(start_date), days_ahead=6)
    log.info('[DiD: %d] Prediction pipeline finished.', device['_device_id'])

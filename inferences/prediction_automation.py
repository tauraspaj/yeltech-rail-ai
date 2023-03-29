from inferences.model_predictions import prediction_pipeline
from common.sql import Devices
from datetime import date

# Fetch all device ids from the database
device_ids = Devices().get_all()

start_date = date.today()

for device in device_ids:
    print(f"\n[DiD: {device['_device_id']}] Starting prediction pipeline.")

    if device['prediction_status'] == 0:
        print(f"[DiD: {device['_device_id']}] Prediction status 0. Skipping..")
        continue

    prediction_pipeline(device['_device_id'], str(start_date), days_ahead=6)
    print(f"[DiD: {device['_device_id']}] Prediction pipeline finished!")

import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

from common import logger, utils

log = logger.get_logger()
load_dotenv()


class Sql:
    def __init__(self):
        self.conn = self.__open_connection()
        self._cursor = self.conn.cursor(dictionary=True, buffered=True)

    def __open_connection(self):
        try:
            return mysql.connector.connect(host=os.getenv('DB_ENDPOINT'),
                                           user=os.getenv('DB_USERNAME'),
                                           password=os.getenv('DB_PASSWORD'),
                                           database='yeltech_ai_db')
        except mysql.connector.Error as error:
            raise Exception(f'Unable to connect to the database: {error}')

    def fetch_one(self, query):
        self._cursor.execute(query)
        return self._cursor.fetchone()

    def fetch_all(self, query):
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def execute_query(self, query):
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def insert_query(self, query, values=None):
        if values:
            self._cursor.execute(query, values)
        else:
            self._cursor.execute(query)
        self.conn.commit()
        return self._cursor.lastrowid

    def __del__(self):
        self.conn.close()


class PredParams(Sql):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return self.fetch_all(
            '''
            SELECT *
            FROM prediction_parameters
            ''')

    def get_one(self, parameter_id):
        return self.fetch_one(
            f'''
            SELECT *
            FROM prediction_parameters
            WHERE _parameter_id = {parameter_id}
            ''')

    def get_all_provider_parameters(self, provider):
        return self.fetch_all(
            f'''
            SELECT *
            FROM prediction_parameters
            WHERE param_provider = "{provider}"
            ''')


class Devices(Sql):
    def __init__(self):
        super().__init__()

    def get_one(self, device_id):
        return self.fetch_one(
            f'''
            SELECT *
            FROM devices
            WHERE devices._device_id = {device_id}
            ''')

    def get_all(self):
        return self.fetch_all(
            '''
            SELECT *
            FROM devices
            ''')

    def get_model(self, device_id):
        model_id = self.get_one(device_id)['model_id']
        return self.fetch_one(
            f'''
            SELECT models.model_file_name
            FROM models
            WHERE models._model_id = {model_id}
            ''')['model_file_name']


class Models(Sql):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return self.fetch_all(
            '''
            SELECT *
            FROM models
            ''')

    def get_one(self, model_id):
        return self.fetch_one(
            f'''
            SELECT *
            FROM models
            WHERE _model_id = {model_id}
            ''')

    def get_model_parameters(self, model_id):
        model_params = self.fetch_all(
            f'''
            SELECT prediction_parameters.parameter_name
            FROM model_parameters
            LEFT JOIN prediction_parameters
            ON model_parameters.prediction_parameter_id
                        = prediction_parameters._parameter_id
            WHERE model_parameters.model_id = {model_id};
            ''')
        return [param['parameter_name'] for param in model_params]


def save_predictions_to_db(predictions, all_data,
                           time_of_execution, device_id):
    device_data = Devices().get_one(device_id)
    model_data = Models().get_one(device_data['model_id'])

    predictions_df = pd.DataFrame(predictions)
    predictions_df = predictions_df.rename(columns={'timestamp': 'time'})
    predictions_df['time'] = pd.to_datetime(predictions_df['time'])

    log.info(
        "[DiD %d] Attempting to insert predictions to database. "
        "Shape %s", device_id, predictions_df.shape)

    try:
        new_prediction_rows = []
        for _, row in predictions_df.iterrows():
            predictions_table_sql = '''
                INSERT INTO predictions (time_of_execution, prediction,
                prediction_timestamp, latitude, longitude, model_id, device_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
            values = (
                time_of_execution, float(row['reading']), row['time'],
                device_data['latitude'], device_data['longitude'],
                device_data['model_id'], device_id
            )

            # Execute the INSERT statement
            new_row_id = Sql().insert_query(predictions_table_sql, values)

            # Collect the new row id that will be used for parameter history
            new_prediction_rows.append({
                'time': row['time'],
                'new_prediction_row_id': new_row_id
            })

        log.info("Predictions saved successfully.")
    except Exception as e:
        log.error(
            "Failed to save predictions to database. "
            "Ending process. Error: %s", e)
        return

    # Find param ids
    provider_dict = utils.convert_model_param_list_to_dict(
        PredParams().get_all_provider_parameters(
            model_data['param_provider']
        )
    )
    manual_params = utils.convert_model_param_list_to_dict(
        PredParams().get_all_provider_parameters(
            'Manual'
        )
    )
    # Join param dicts
    param_dict = {**provider_dict, **manual_params}

    log.info(
        "[DiD %d] Attempting to insert parameter history to database. "
        "Shape %s", device_id, all_data.shape)

    insert_parameter_history_data(all_data, param_dict, new_prediction_rows)

    return


def insert_parameter_history_data(all_data, param_dict, new_prediction_rows):
    prediction_ids_df = pd.DataFrame(new_prediction_rows)

    # Add to parameter_history table
    parameter_history_table_sql = '''
        INSERT INTO parameter_history (parameter_value, parameter_id,
        prediction_id)
        VALUES
        '''

    for _, row in all_data.iterrows():
        time = row.loc['time']
        prediction_id = prediction_ids_df.loc[
            prediction_ids_df['time'] == time, 'new_prediction_row_id'].item()

        for column_name, cell_value in row.items():
            if column_name != 'time':
                values = (cell_value, param_dict[column_name], prediction_id)
                parameter_history_table_sql += f"{str(values)},"

    # Delete the last comma
    parameter_history_table_sql = parameter_history_table_sql[:-1]
    try:
        Sql().insert_query(parameter_history_table_sql)
        log.info("Parameter history saved successfully.")
    except Exception as e:
        log.error(
            "Failed to save parameter history to database. "
            "Ending process. Error: %s", e)
        return
    return

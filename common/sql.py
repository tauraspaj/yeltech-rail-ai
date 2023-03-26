import mysql.connector
from dotenv import dotenv_values

ENV = dotenv_values(".env")


class Sql:
    def __init__(self):
        self.conn = self.__open_connection()
        self._cursor = self.conn.cursor(dictionary=True)

    def __open_connection(self):
        try:
            return mysql.connector.connect(host=ENV['DB_ENDPOINT'],
                                           user=ENV['DB_USERNAME'],
                                           password=ENV['DB_PASSWORD'],
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

    def __del__(self):
        self.conn.close()


class PredParams(Sql):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return self.fetch_all(
            '''
            SELECT _parameter_id, parameter_name, unit, param_provider
            FROM prediction_parameters
            ''')

    def get_one(self, parameter_id):
        return self.fetch_one(
            f'''
            SELECT _parameter_id, parameter_name, unit, param_provider
            FROM prediction_parameters
            WHERE _parameter_id = {parameter_id}
            ''')

    def get_all_openmeteo_parameters(self):
        result = self.fetch_all(
            '''
            SELECT parameter_name
            FROM prediction_parameters
            WHERE param_provider = "Open-Meteo"
            ''')
        return [r['parameter_name'] for r in result]


class Devices(Sql):
    def __init__(self):
        super().__init__()

    def get_one(self, device_id):
        return self.fetch_one(
            f'''
            SELECT _device_id, device_name, prediction_status, latitude,
            longitude, model_id
            FROM devices
            WHERE devices._device_id = {device_id}
            ''')

    def get_all(self):
        return self.fetch_all(
            '''
            SELECT _device_id, device_name, prediction_status, latitude,
            longitude, model_id FROM devices
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
            SELECT _model_id, model_file_name
            FROM models
            ''')

    def get_one(self, model_id):
        return self.fetch_one(
            f'''
            SELECT _model_id, model_file_name
            FROM models
            WHERE _model_id = {model_id}
            ''')

    def get_model_parameters(self, model_id):
        model_params = self.execute_query(
            f'''
            SELECT prediction_parameters.parameter_name
            FROM model_parameters
            LEFT JOIN prediction_parameters
            ON model_parameters.prediction_parameter_id
                        = prediction_parameters._parameter_id;
            WHERE model_parameters.model_id = {model_id};
            ''')
        return [param['parameter_name'] for param in model_params]

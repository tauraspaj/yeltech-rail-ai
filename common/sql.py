import mysql.connector
from dotenv import dotenv_values

ENV = dotenv_values(".env")


class Sql:
    def __init__(self):
        self.conn = self.__open_connection()
        self._cursor = self.conn.cursor()

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
        return self.fetch_all('SELECT * FROM prediction_parameters')

    def get_all_openmeteo_names(self):
        result = self.fetch_all('''SELECT parameter_name
                FROM prediction_parameters
                WHERE param_provider = "Open-Meteo"
            ''')
        return [r[0] for r in result]


class Devices(Sql):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return self.fetch_all('SELECT * FROM devices')


class Models(Sql):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return self.fetch_all('SELECT * FROM models')

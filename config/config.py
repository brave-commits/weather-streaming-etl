from dotenv import load_dotenv
import os


class LoadParams:
    def __init__(self):
        load_dotenv('.env-app')
        load_dotenv('.env-dbconn')
        self.db_driver = os.environ.get('DB_DRIVER')
        self.db_server = os.environ.get('DB_SERVER')
        self.db_database = os.environ.get('DB_DATABASE')
        self.db_port = os.environ.get('DB_PORT')
        self.db_usr = os.environ.get('DB_USR')
        self.db_pwd = os.environ.get('MSSQL_SA_PASSWORD')
        self.db_table = os.environ.get('DB_TABLE')
        self.db_schema = os.environ.get('DB_SCHEMA')
        self.db_trust_cert = os.environ.get('DB_TRUST_CERT')
        self.weather_api_key = os.environ.get('WEATHER_API_KEY')
        self.weather_url = os.environ.get('WEATHER_URL')
        self.weather_lat = os.environ.get('WEATHER_LAT')
        self.weather_lon = os.environ.get('WEATHER_LON')
        self.weather_units = os.environ.get('WEATHER_UNITS')
        self.kafka_bootstrap = os.environ.get('KAFKA_BOOTSTRAP')
        self.kafka_group = os.environ.get('KAFKA_GROUP')
        self.kafka_offset = os.environ.get('KAFKA_OFFSET')
        self.kafka_topic = os.environ.get('KAFKA_TOPIC')

class ParamsFactory:
    @classmethod
    def create_params(self):
        params = LoadParams()
        return params
    
import requests
from config.config import ParamsFactory
from utils.logger import Logger

def get_request():
    try:
        params = ParamsFactory.create_params()
        url = params.weather_url
        params = {
            'lat': params.weather_lat,
            'lon': params.weather_lon,
            'units': params.weather_units,
            'appid': params.weather_api_key

        }
        get = requests.get(url, params=params)
        response = get.json()
        status_code = get.status_code
        if 'message' in response and response['message'] is not None:
            log_response = response['message']
        else:
            log_response = 'OK'
        log_message = f'GET request returned with status code {status_code}: {log_response}'
        Logger.log_info(log_message)
        return response
    
    except Exception as e:
        Logger.log_error(e)

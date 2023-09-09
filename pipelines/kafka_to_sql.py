import requests
#from config.config import ParamsFactory
from utils.logging import Logger
from utils.api import get_request
from utils.kafka import producer, consumer

resp = get_request()
producer(resp)


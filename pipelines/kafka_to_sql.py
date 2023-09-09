from utils.api import get_request
from utils.kafka import producer, consumer
import time

def weather_pub_sub():
    while True:
        resp = get_request()
        producer(resp)
        consumer()
        time.sleep(600)


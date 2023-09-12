from utils.api import get_request
from utils.kafka import producer, consumer
from utils.datagen import get_random_us_coordinate
import time
import threading
import uuid


def producer_thread(message_id):
    random_coordinate = get_random_us_coordinate()
    lat = random_coordinate['latitude']
    long = random_coordinate['longitude']
    resp = get_request(lat, long)
    producer(resp, message_id)

def consumer_thread(message_id):
    time.sleep(5)
    consumer(message_id)


def weather_pub_sub():
    while True:
        message_id = uuid.uuid4()
        producer_thread_instance = threading.Thread(target=producer_thread, args=(message_id,))
        consumer_thread_instance = threading.Thread(target=consumer_thread, args=(message_id,))
        producer_thread_instance.start()
        consumer_thread_instance.start()
        producer_thread_instance.join()
        consumer_thread_instance.join()

        time.sleep(1)

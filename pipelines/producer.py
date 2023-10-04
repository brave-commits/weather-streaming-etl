from utils.api import get_request
from utils.kafka import producer
from utils.datagen import get_random_us_coordinate
from utils.scheduler import scheduler


def send_to_kafka():
    random_coordinate = get_random_us_coordinate()
    lat = random_coordinate['latitude']
    long = random_coordinate['longitude']
    resp = get_request(lat, long)
    producer(resp)


scheduler(send_to_kafka,1)
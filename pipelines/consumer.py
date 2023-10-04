from utils.kafka import consumer
from utils.scheduler import scheduler

scheduler(consumer,5)
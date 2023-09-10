import uuid
import json
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from config.config import ParamsFactory 
from utils.logger import Logger
from utils.database import DBSession
from utils.transform import JsonFlattener, DFConverter
import pandas as pd

params = ParamsFactory.create_params()
message_id = uuid.uuid4()

def producer(data):
    try:
        producer = Producer({'bootstrap.servers': params.kafka_bootstrap})
        topic = params.kafka_topic
        producer.produce(topic, key=None, value=json.dumps(data))
        producer.flush()
        Logger.log_info(f'Data sent to {topic} | {message_id}')

    except Exception as e:
        Logger.log_error(f'Failed to send data to {topic}: {e} | {message_id}')

def consumer():
    try:
        consumer = Consumer(
            {
                'bootstrap.servers': params.kafka_bootstrap,
                'group.id': params.kafka_group,
                'auto.offset.reset': params.kafka_offset
            }
        )
        topic = params.kafka_topic
        consumer.subscribe([topic])
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    partition_end = f"%% {msg.topic()} [{msg.partition()}] reached end of offset {msg.offset()}"
                    Logger.log_info(partition_end)
                else:
                    raise KafkaException(msg.error())
            log_message = f'{msg.topic()} consumed | {message_id}'
            Logger.log_info(log_message)
            df_message= msg.value().decode('utf-8')
            json_flat = JsonFlattener.flatten(df_message)
            df = DFConverter.convert_json(json_flat)
            db_session = DBSession.create_session()
            session = db_session.session
            

          
        
    except Exception as e:
        Logger.log_error(e)

    finally:
        Logger.log_info("job shutting down.")

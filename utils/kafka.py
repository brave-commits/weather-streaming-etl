import uuid
import json
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
from config.config import ParamsFactory 
from utils.logger import Logger
from utils.transform import flatten, json_to_df 
from utils.database import DBSession
import ast
import time 

params = ParamsFactory.create_params()


def producer(data, message_id):
    try:
        producer = Producer({'bootstrap.servers': params.kafka_bootstrap})
        topic = params.kafka_topic
        producer.produce(topic, key=None, value=json.dumps(data))
        producer.flush()
        Logger.log_info(f'Data sent to {topic} | {message_id}')

    except Exception as e:
        Logger.log_error(f'Failed to send data to {topic}: {e} | {message_id}')

def consumer(message_id):
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
        start_time = time.time() 
        
        while True:
            current_time = time.time()
            if current_time - start_time >= 30:
                break
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    partition_end = f"%% {msg.topic()} [{msg.partition()}] reached end of offset {msg.offset()}"
                    Logger.log_info(partition_end)
                    break
                else:
                    raise KafkaException(msg.error())
            else:
                log_message = f'{msg.topic()} consumed | {message_id}'
                Logger.log_info(log_message)
                json_message= msg.value().decode('utf-8')
                json_message_dict = ast.literal_eval(json_message)
                flat_json = flatten(json_message_dict)
                Logger.log_info(f'JSON response flattened. | {message_id}')
                df = json_to_df(flat_json)
                Logger.log_info(f'Dataframe successfully created.| {message_id}')
                DBSession.df_to_sql(df)
                Logger.log_info(f'Dataframe inserted into {params.db_schema}.{params.db_table}. | {message_id}')
        
    except Exception as e:
        Logger.log_error(e)

    finally:
        Logger.log_info("All available messages consumed.")

import json
from collections.abc import AsyncGenerator

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from config.settings import settings
from utils.logger import logger


async def produce(message: dict) -> None:
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap)
    await producer.start()
    try:
        await producer.send_and_wait(
            settings.kafka_topic,
            json.dumps(message).encode(),
        )
        logger.info("message_produced", topic=settings.kafka_topic)
    finally:
        await producer.stop()


async def consume_stream() -> AsyncGenerator[dict, None]:
    consumer = AIOKafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap,
        group_id=settings.kafka_group,
        auto_offset_reset=settings.kafka_offset,
        value_deserializer=lambda v: json.loads(v.decode()),
    )
    await consumer.start()
    try:
        async for msg in consumer:
            logger.info("message_consumed", topic=msg.topic, offset=msg.offset)
            yield msg.value
    finally:
        await consumer.stop()

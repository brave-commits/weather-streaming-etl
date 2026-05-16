from utils.database import insert_reading
from utils.kafka import consume_stream
from utils.logger import logger


async def consume_loop() -> None:
    logger.info("consumer_started")
    async for message in consume_stream():
        try:
            await insert_reading(message)
            logger.info("record_inserted", city=message.get("city"))
        except Exception:
            logger.exception("consumer_error")

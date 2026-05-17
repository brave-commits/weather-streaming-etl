import asyncio

from config.settings import settings
from utils.api import fetch_weather
from utils.datagen import get_random_us_coordinate
from utils.kafka import produce
from utils.logger import logger


async def produce_loop() -> None:
    logger.info("producer_started", interval=settings.produce_interval)
    while True:
        try:
            coord = get_random_us_coordinate()
            raw = await fetch_weather(coord["latitude"], coord["longitude"])  # type: ignore[arg-type]
            message = {
                "city": coord["city"],
                "latitude": coord["latitude"],
                "longitude": coord["longitude"],
                "data": raw,
            }
            await produce(message)
        except Exception:
            logger.exception("producer_error")
        await asyncio.sleep(settings.produce_interval)

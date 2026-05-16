import asyncio

from pipelines.consumer import consume_loop
from pipelines.producer import produce_loop
from utils.database import init_db
from utils.logger import logger


async def main() -> None:
    await init_db()
    logger.info("pipeline_started")
    await asyncio.gather(produce_loop(), consume_loop())


if __name__ == "__main__":
    asyncio.run(main())

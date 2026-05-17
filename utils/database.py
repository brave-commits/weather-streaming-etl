import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config.settings import settings


class Base(DeclarativeBase):
    pass


class WeatherReading(Base):
    __tablename__ = "weather_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    raw: Mapped[dict] = mapped_column(JSONB)
    recorded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


engine: AsyncEngine = create_async_engine(settings.db_url, echo=False)
_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_reading(message: dict) -> None:
    reading = WeatherReading(
        city=message["city"],
        latitude=message["latitude"],
        longitude=message["longitude"],
        raw=message["data"],
    )
    async with _session_factory() as session:
        async with session.begin():
            session.add(reading)

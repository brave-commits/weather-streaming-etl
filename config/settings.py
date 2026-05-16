from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Weather API
    weather_api_key: str
    weather_url: str = "https://api.openweathermap.org/data/2.5/weather"
    weather_units: str = "imperial"

    # Kafka
    kafka_bootstrap: str
    kafka_topic: str
    kafka_group: str = "weather-consumer"
    kafka_offset: str = "earliest"

    # Database (postgresql+asyncpg://user:pass@host/db)
    db_url: str

    # Pipeline
    produce_interval: float = 1.0


settings = Settings()

import os

import pytest

# Provide required settings so the module-level `settings = Settings()` succeeds
# when tests are collected without a real .env file present.
os.environ.setdefault("WEATHER_API_KEY", "test-key")
os.environ.setdefault("KAFKA_BOOTSTRAP", "localhost:9092")
os.environ.setdefault("KAFKA_TOPIC", "weather-test")
os.environ.setdefault("DB_URL", "postgresql+asyncpg://user:pass@localhost/test")

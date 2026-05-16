import pytest
from pydantic import ValidationError

from config.settings import Settings


def test_settings_accepts_valid_config():
    s = Settings(
        weather_api_key="test-key",
        kafka_bootstrap="localhost:9092",
        kafka_topic="weather",
        db_url="postgresql+asyncpg://user:pass@localhost/db",
    )
    assert s.weather_units == "imperial"
    assert s.produce_interval == 1.0
    assert s.kafka_group == "weather-consumer"
    assert s.kafka_offset == "earliest"


def test_settings_rejects_missing_required_fields():
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,  # type: ignore[call-arg]
            weather_api_key=None,  # type: ignore[arg-type]
            kafka_bootstrap=None,  # type: ignore[arg-type]
            kafka_topic=None,  # type: ignore[arg-type]
            db_url=None,  # type: ignore[arg-type]
        )


def test_produce_interval_defaults_to_one_second():
    s = Settings(
        weather_api_key="k",
        kafka_bootstrap="b:9092",
        kafka_topic="t",
        db_url="postgresql+asyncpg://u:p@h/d",
    )
    assert s.produce_interval == 1.0


def test_produce_interval_is_configurable():
    s = Settings(
        weather_api_key="k",
        kafka_bootstrap="b:9092",
        kafka_topic="t",
        db_url="postgresql+asyncpg://u:p@h/d",
        produce_interval=5.0,
    )
    assert s.produce_interval == 5.0

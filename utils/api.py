import httpx

from config.settings import settings
from utils.logger import logger


async def fetch_weather(lat: float, lon: float) -> dict:
    params = {
        "lat": lat,
        "lon": lon,
        "units": settings.weather_units,
        "appid": settings.weather_api_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.weather_url, params=params)
        response.raise_for_status()
    data: dict = response.json()
    logger.info("weather_fetched", status=response.status_code, city=data.get("name"))
    return data

"""Constants in weatherbit component."""
import logging

from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN

ATTR_WEATHERBIT_AQI = "aqi"
ATTR_WEATHERBIT_CLOUDINESS = "cloudiness"
ATTR_WEATHERBIT_IS_NIGHT = "is_night"
ATTR_WEATHERBIT_WIND_GUST = "wind_gust"
ATTR_WEATHERBIT_PRECIPITATION = "precipitation"
ATTR_WEATHERBIT_UVI = "uv_index"
ATTR_WEATHERBIT_UPDATED = "updated"

DOMAIN = "weatherbit"

DEVICE_TYPE_TEMPERATURE = "temperature"
DEVICE_TYPE_WIND = "wind"
DEVICE_TYPE_RAIN = "rain"
DEVICE_TYPE_PRESSURE = "pressure"
DEVICE_TYPE_HUMIDITY = "humidity"
DEVICE_TYPE_WEATHER = "weather"
DEVICE_TYPE_DISTANCE = "distance"
DEVICE_TYPE_NONE = "none"

WEATHERBIT_PLATFORMS = [
    "weather",
    "sensor",
]

DEFAULT_ATTRIBUTION = "Data provided by Weatherbit.io"
DEFAULT_BRAND = "Weatherbit.io"

LOGGER = logging.getLogger(__package__)

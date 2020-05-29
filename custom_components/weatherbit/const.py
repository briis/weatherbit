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

CONF_ADD_SENSORS = "add_sensors"

DOMAIN = "weatherbit"

DEVICE_TYPE_TEMPERATURE = "temperature"
DEVICE_TYPE_WIND = "wind"
DEVICE_TYPE_RAIN = "rain"
DEVICE_TYPE_PRESSURE = "pressure"
DEVICE_TYPE_HUMIDITY = "humidity"
DEVICE_TYPE_WEATHER = "weather"
DEVICE_TYPE_DISTANCE = "distance"

TYPE_SENSOR = "sensor"
TYPE_FORECAST = "forecast"

WEATHERBIT_PLATFORMS = [
    "weather",
    "sensor",
]

CONDITION_CLASSES = {
    "clear-night": [8000],
    "cloudy": [803, 804],
    "exceptional": [],
    "fog": [741],
    "hail": [623],
    "lightning": [230, 231],
    "lightning-rainy": [200, 201, 202],
    "partlycloudy": [801, 802],
    "pouring": [502, 522],
    "rainy": [300, 301, 302, 500, 501, 511, 520, 521],
    "snowy": [600, 601, 602, 621, 622, 623],
    "snowy-rainy": [610, 611, 612],
    "sunny": [800],
    "windy": [],
    "windy-variant": [],
}

DEFAULT_ATTRIBUTION = "Data provided by Weatherbit.io"
DEFAULT_BRAND = "Weatherbit.io"

LOGGER = logging.getLogger(__package__)

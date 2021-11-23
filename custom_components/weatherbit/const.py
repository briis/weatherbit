"""Constants in weatherbit component."""

ATTR_WEATHERBIT_AQI = "aqi"
ATTR_WEATHERBIT_ALERTS = "alerts"
ATTR_WEATHERBIT_CLOUDINESS = "cloudiness"
ATTR_WEATHERBIT_IS_NIGHT = "is_night"
ATTR_WEATHERBIT_WIND_GUST = "wind_gust"
ATTR_WEATHERBIT_PRECIPITATION = "precipitation"
ATTR_WEATHERBIT_SNOW = "snow"
ATTR_WEATHERBIT_UVI = "uv_index"
ATTR_WEATHERBIT_UPDATED = "updated"
ATTR_WEATHERBIT_FCST_POP = "precip_prob"
ATTR_WEATHERBIT_WEATHER_TEXT = "weather_text"
ATTR_WEATHERBIT_WEATHER_ICON = "weather_icon"
ATTR_WEATHERBIT_ALT_CONDITION = "alt_condition"

CONF_INTERVAL_SENSORS = "update_interval"
CONF_INTERVAL_FORECAST = "forecast_interval"
CONF_FORECAST_LANGUAGE = "forecast_language"
CONFIG_OPTIONS = [
    CONF_FORECAST_LANGUAGE,
    CONF_INTERVAL_FORECAST,
    CONF_INTERVAL_SENSORS,
]

DEFAULT_ATTRIBUTION = "Powered by Weatherbit.io"
DEFAULT_INTERVAL_SENSORS = 5
DEFAULT_INTERVAL_FORECAST = 30
DEFAULT_BRAND = "Weatherbit.io"
DEFAULT_FORECAST_LANGUAGE = "en"

DOMAIN = "weatherbit"

DEVICE_CLASS_LOCAL_ALERTS = "alerts"
DEVICE_CLASS_LOCAL_BEAUFORT = "beaufort"
DEVICE_CLASS_LOCAL_WIND_CARDINAL = "wind_cardinal"

DEVICE_TYPE_TEMPERATURE = "temperature"
DEVICE_TYPE_WIND = "wind"
DEVICE_TYPE_RAIN = "rain"
DEVICE_TYPE_SNOW = "snow"
DEVICE_TYPE_PRESSURE = "pressure"
DEVICE_TYPE_HUMIDITY = "humidity"
DEVICE_TYPE_WEATHER = "weather"
DEVICE_TYPE_DISTANCE = "distance"

TYPE_SENSOR = "sensor"
TYPE_FORECAST = "forecast"
TYPE_ALERT = "alert"

UNIT_WIND_MS = "m/s"
UNIT_WIND_KMH = "km/h"
UNIT_WIND_KNOT = "knot"
WIND_UNITS = [
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
]

WEATHERBIT_API_VERSION = "2.0"
WEATHERBIT_PLATFORMS = [
    # "weather",
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

ALT_CONDITION_CLASSES = {
    "partlycloudy-night": [8010, 8020],
    "clear-night": [8000],
    "cloudy": [803, 804],
    "exceptional": [],
    "fog": [741],
    "hail": [623],
    "lightning": [230, 231],
    "lightning-rainy": [200, 201, 202],
    "partlycloudy-day": [801, 802],
    "pouring": [502, 522],
    "rainy": [300, 301, 302, 500, 501, 511, 520, 521],
    "snowy": [600, 601, 602, 621, 622, 623],
    "snowy-rainy": [610, 611, 612],
    "sunny": [800],
    "windy": [],
    "windy-variant": [],
}

MDI_CONDITION_CLASSES = {
    "weather-night-partly-cloudy": [8010, 8020],
    "weather-night": [8000],
    "weather-cloudy": [803, 804],
    "exceptional": [],
    "weather-fog": [741],
    "weather-hail": [623],
    "weather-lightning": [230, 231],
    "weather-lightning-rainy": [200, 201, 202],
    "weather-partly-cloudy": [801, 802],
    "weather-pouring": [502, 522],
    "weather-rainy": [300, 301, 302, 500, 501, 511, 520, 521],
    "weather-snowy": [600, 601, 602, 621, 622, 623],
    "weather-snowy-rainy": [610, 611, 612],
    "weather-sunny": [800],
    "weather-windy": [],
}

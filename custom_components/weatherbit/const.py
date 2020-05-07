"""Constants in weatherbit component."""
import logging

from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN

ATTR_WEATHERBIT_CLOUDINESS = "cloudiness"
ATTR_WEATHERBIT_WIND_GUST = "wind_gust"

DOMAIN = "weatherbit"

HOME_LOCATION_NAME = "Home"

ENTITY_ID_SENSOR_FORMAT = WEATHER_DOMAIN + ".weatherbit_{}"
ENTITY_ID_SENSOR_FORMAT_HOME = ENTITY_ID_SENSOR_FORMAT.format(HOME_LOCATION_NAME)

DEFAULT_ATTRIBUTION = "Data provided by Weatherbit.io"

LOGGER = logging.getLogger(__package__)

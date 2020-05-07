"""Constants in weatherbit component."""
import logging

from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN

ATTR_WEATHERBIT_CLOUDINESS = "cloudiness"

DOMAIN = "weatherbit"

HOME_LOCATION_NAME = "Home"

ENTITY_ID_SENSOR_FORMAT = WEATHER_DOMAIN + ".weatherbit_{}"
ENTITY_ID_SENSOR_FORMAT_HOME = ENTITY_ID_SENSOR_FORMAT.format(HOME_LOCATION_NAME)

LOGGER = logging.getLogger(__package__)
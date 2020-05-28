"""Weatherbit Sensors for Home Assistant."""

import logging

from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util.pressure import convert as convert_pressure
from homeassistant.util.distance import convert as convert_distance
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    LENGTH_METERS,
    LENGTH_MILES,
    LENGTH_KILOMETERS,
    PRESSURE_HPA,
    PRESSURE_INHG,
    TEMP_CELSIUS,
)
from .const import (
    DOMAIN,
    ATTR_WEATHERBIT_UPDATED,
    DEFAULT_ATTRIBUTION,
    DEVICE_TYPE_TEMPERATURE,
    DEVICE_TYPE_WIND,
    DEVICE_TYPE_HUMIDITY,
    DEVICE_TYPE_RAIN,
    DEVICE_TYPE_PRESSURE,
    DEVICE_TYPE_DISTANCE,
)
from .entity import WeatherbitEntity

SENSORS = {
    "temp": ["Temperature", DEVICE_TYPE_TEMPERATURE, "thermometer"],
    "wind_spd": ["Wind Speed", DEVICE_TYPE_WIND, "weather-windy"],
    "app_temp": ["Apparent Temperature", DEVICE_TYPE_TEMPERATURE, "thermometer"],
    "humidity": ["Humidity", DEVICE_TYPE_HUMIDITY, "water-percent"],
    "pres": ["Pressure", DEVICE_TYPE_PRESSURE, "gauge"],
    "clouds": ["Cloud Coverage", "%", "cloud-outline"],
    "solar_rad": ["Solar Radiation", "W/m2", "weather-sunny"],
    "wind_cdir": ["Wind Direction", "", "compass-outline"],
    "wind_dir": ["Wind Bearing", "°", "compass-outline"],
    "dewpt": ["Dewpoint", DEVICE_TYPE_TEMPERATURE, "thermometer"],
    "vis": ["Visibility", DEVICE_TYPE_DISTANCE, "eye-outline"],
    "precip": ["Rain Today", DEVICE_TYPE_RAIN, "weather-rainy"],
    "uv": ["UV Index", "UVI", "weather-sunny-alert"],
    "aqi": ["Air Quality", "AQI", "hvac"],
}

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Setup the Weatherbit sensor platform."""

    fcst_coordinator = hass.data[DOMAIN][entry.entry_id]["fcst_coordinator"]
    if not fcst_coordinator.data:
        return

    cur_coordinator = hass.data[DOMAIN][entry.entry_id]["cur_coordinator"]
    if not cur_coordinator.data:
        return

    sensors = []
    for sensor in SENSORS:
        sensors.append(
            WeatherbitSensor(
                fcst_coordinator,
                cur_coordinator,
                entry.data,
                sensor,
                hass.config.units.is_metric,
            )
        )

    async_add_entities(sensors, True)

    return True


class WeatherbitSensor(WeatherbitEntity, Entity):
    """Implementation of Weatherbit sensor."""

    def __init__(self, fcst_coordinator, cur_coordinator, entries, sensor, is_metric):
        """Initialize Weatherbit sensor."""
        super().__init__(fcst_coordinator, cur_coordinator, entries, sensor)
        self._sensor = sensor
        self._is_metric = is_metric
        self._device_class = SENSORS[self._sensor][1]
        self._name = f"{DOMAIN.capitalize()} {SENSORS[self._sensor][0]}"
        self._unique_id = f"{self._device_key}_{self._sensor}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        value = getattr(self._current, self._sensor)
        if self._device_class == DEVICE_TYPE_WIND:
            if self._is_metric:
                return round(value, 1)
            else:
                return round(float(value * 2.23693629), 2)
        elif self._device_class == DEVICE_TYPE_PRESSURE:
            if self._is_metric:
                return value
            else:
                return round(convert_pressure(value, PRESSURE_HPA, PRESSURE_INHG), 2)
        elif self._device_class == DEVICE_TYPE_RAIN:
            if self._is_metric:
                return round(float(value), 1)
            else:
                round(float(value) / 25.4, 2)
        elif self._device_class == DEVICE_TYPE_DISTANCE:
            if self._is_metric:
                return value
            else:
                return int(
                    float(convert_distance(value, LENGTH_KILOMETERS, LENGTH_MILES))
                )
        elif self._device_class == "UVI":
            return round(float(value), 1)
        else:
            return value

    @property
    def icon(self):
        """Return icon for sensor."""
        return f"mdi:{SENSORS[self._sensor][2]}"

    @property
    def unit_of_measurement(self):
        """Return the units of measurement."""
        if self._device_class == DEVICE_TYPE_TEMPERATURE:
            return TEMP_CELSIUS
        elif self._device_class == DEVICE_TYPE_WIND:
            return "m/s" if self._is_metric else "mi/h"
        elif self._device_class == DEVICE_TYPE_PRESSURE:
            return "hPa" if self._is_metric else "inHg"
        elif self._device_class == DEVICE_TYPE_HUMIDITY:
            return "%"
        elif self._device_class == DEVICE_TYPE_RAIN:
            return "mm" if self._is_metric else "in"
        elif self._device_class == DEVICE_TYPE_DISTANCE:
            return "km" if self._is_metric else "mi"
        else:
            return self._device_class

    @property
    def device_state_attributes(self):
        """Return Weatherbit specific attributes."""
        return {
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
            ATTR_WEATHERBIT_UPDATED: getattr(self._current, "obs_time_local"),
        }

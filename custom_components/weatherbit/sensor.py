"""Weatherbit Sensors for Home Assistant."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    DEGREE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_TIMESTAMP,
    DEVICE_CLASS_VOLTAGE,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import StateType

from .const import (
    DOMAIN,
    DEVICE_CLASS_LOCAL_ALERTS,
    DEVICE_CLASS_LOCAL_WIND_CARDINAL,
    DEVICE_CLASS_LOCAL_BEAUFORT,
)
from .entity import WeatherbitEntity
from .models import WeatherBitEntryData


@dataclass
class WeatherBitRequiredKeysMixin:
    """Mixin for required keys."""

    unit_type: str
    extra_attributes: bool


@dataclass
class WeatherBitSensorEntityDescription(
    SensorEntityDescription, WeatherBitRequiredKeysMixin
):
    """Describes WeatherBit Sensor entity."""


SENSOR_TYPES: tuple[WeatherBitSensorEntityDescription, ...] = (
    WeatherBitSensorEntityDescription(
        key="temp",
        name="Air Temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="app_temp",
        name="Apparent Temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up sensors for WeatherFlow integration."""
    entry_data: WeatherBitEntryData = hass.data[DOMAIN][entry.entry_id]
    weatherbitapi = entry_data.weatherbitapi
    coordinator = entry_data.coordinator
    forecast_coordinator = entry_data.forecast_coordinator
    station_data = entry_data.station_data
    unit_descriptions = entry_data.unit_descriptions

    entities = []
    for description in SENSOR_TYPES:
        entities.append(
            WeatherbitSensor(
                weatherbitapi,
                coordinator,
                forecast_coordinator,
                station_data,
                description,
                entry,
                unit_descriptions,
            )
        )

        _LOGGER.debug(
            "Adding sensor entity %s",
            description.name,
        )

    async_add_entities(entities)


class WeatherbitSensor(WeatherbitEntity, SensorEntity):
    """Implementation of Weatherbit sensor."""

    def __init__(
        self,
        weatherbitapi,
        coordinator,
        forecast_coordinator,
        station_data,
        description,
        entries: ConfigEntry,
        unit_descriptions,
    ):
        """Initialize an WeatherFlow sensor."""
        super().__init__(
            weatherbitapi,
            coordinator,
            forecast_coordinator,
            station_data,
            description,
            entries,
        )
        self._attr_name = f"{DOMAIN.capitalize()} {self.entity_description.name}"
        if self.entity_description.native_unit_of_measurement is None:
            self._attr_native_unit_of_measurement = unit_descriptions[
                self.entity_description.unit_type
            ]

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""

        return (
            getattr(self.coordinator.data, self.entity_description.key)
            if self.coordinator.data
            else None
        )

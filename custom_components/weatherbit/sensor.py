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
    DEVICE_CLASS_AQI,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import StateType
from pyweatherbitdata.data import AlertDescription

from .const import (
    ATTR_ALERT_DESCRIPTION_EN,
    ATTR_ALERT_DESCRIPTION_LOC,
    ATTR_ALERT_EFFECTIVE,
    ATTR_ALERT_ENDS,
    ATTR_ALERT_EXPIRES,
    ATTR_ALERT_ONSET,
    ATTR_ALERT_REGIONS,
    ATTR_ALERT_SEVERITY,
    ATTR_ALERT_TITLE,
    ATTR_ALERT_URI,
    ATTR_ALERTS,
    ATTR_AQI_LEVEL,
    DEVICE_CLASS_LOCAL_BEAUFORT,
    DEVICE_CLASS_LOCAL_UV_DESCRIPTION,
    DEVICE_CLASS_LOCAL_WIND_CARDINAL,
    DOMAIN,
)
from .entity import WeatherbitEntity
from .models import WeatherBitEntryData

_KEY_ALERTS = "alerts"
_KEY_AQI = "aqi"


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
    WeatherBitSensorEntityDescription(
        key="slp",
        name="Sea Level Pressure",
        device_class=DEVICE_CLASS_PRESSURE,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="pressure",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="humidity",
        name="Relative Humidity",
        native_unit_of_measurement="%",
        device_class=DEVICE_CLASS_HUMIDITY,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="pres",
        name="Station Pressure",
        device_class=DEVICE_CLASS_PRESSURE,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="pressure",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="clouds",
        name="Cloud Coverage",
        native_unit_of_measurement="%",
        icon="mdi:cloud",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="solar_rad",
        name="Solar Radiation",
        icon="mdi:solar-power",
        native_unit_of_measurement="W/m^2",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="wind_spd",
        name="Wind Speed",
        icon="mdi:weather-windy-variant",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="length",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="wind_spd_kmh",
        name="Wind Speed (km/h)",
        icon="mdi:weather-windy-variant",
        native_unit_of_measurement="km/h",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="wind_spd_knots",
        name="Wind Speed (knots)",
        icon="mdi:tailwind",
        native_unit_of_measurement="knots",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="wind_dir",
        name="Wind Direction",
        icon="mdi:compass",
        native_unit_of_measurement=DEGREE,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="wind_cdir",
        name="Wind Cardinal",
        icon="mdi:compass",
        device_class=DEVICE_CLASS_LOCAL_WIND_CARDINAL,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="dewpt",
        name="Dew Point",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="weather_text",
        name="Weather Description",
        icon="mdi:text-short",
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="vis",
        name="Visibility",
        icon="mdi:eye",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="distance",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="precip",
        name="Precipitation",
        icon="mdi:weather-rainy",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="precipitation",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="snow",
        name="Snow",
        icon="mdi:snowflake",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="precipitation",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="uv",
        name="UV Index",
        icon="mdi:weather-sunny-alert",
        native_unit_of_measurement="UVI",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="uv_description",
        name="UV Description",
        icon="mdi:weather-sunny-alert",
        device_class=DEVICE_CLASS_LOCAL_UV_DESCRIPTION,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="aqi",
        name="Air Quality Index",
        device_class=DEVICE_CLASS_AQI,
        native_unit_of_measurement="AQI",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="beaufort_value",
        name="Beaufort",
        icon="mdi:windsock",
        native_unit_of_measurement="Bft",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="beaufort_text",
        name="Beaufort Description",
        icon="mdi:windsock",
        device_class=DEVICE_CLASS_LOCAL_BEAUFORT,
        unit_type="none",
        extra_attributes=False,
    ),
    WeatherBitSensorEntityDescription(
        key="alerts",
        name="Weather Alerts",
        icon="mdi:alert",
        unit_type="none",
        extra_attributes=True,
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

        if self.entity_description.key == _KEY_ALERTS:
            return getattr(self.coordinator.data, "alert_count")

        return (
            getattr(self.coordinator.data, self.entity_description.key)
            if self.coordinator.data
            else None
        )

    @property
    def extra_state_attributes(self):
        """Return the sensor state attributes."""
        if self.entity_description.key == _KEY_ALERTS:
            data = []
            count = 1
            alerts: AlertDescription = getattr(
                self.coordinator.data, self.entity_description.key
            )
            for item in alerts:
                data.append(
                    {
                        f"Alert No {count}": "-------------------",
                        ATTR_ALERT_TITLE: item.title,
                        ATTR_ALERT_SEVERITY: item.severity,
                        ATTR_ALERT_EFFECTIVE: item.effective_utc,
                        ATTR_ALERT_ONSET: item.onset_utc,
                        ATTR_ALERT_ENDS: item.ends_utc,
                        ATTR_ALERT_EXPIRES: item.expires_utc,
                        ATTR_ALERT_URI: item.uri,
                        ATTR_ALERT_REGIONS: item.regions,
                        ATTR_ALERT_DESCRIPTION_EN: item.en_description,
                        ATTR_ALERT_DESCRIPTION_LOC: item.loc_description,
                    }
                )
                count += 1
            return {
                **super().extra_state_attributes,
                ATTR_ALERTS: data,
            }
        if self.entity_description.key == _KEY_AQI:
            return {
                **super().extra_state_attributes,
                ATTR_AQI_LEVEL: getattr(self.coordinator.data, "aqi_level"),
            }
        return super().extra_state_attributes

"""Support for the Weatherbit weather service."""
from __future__ import annotations

import logging

from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_WIND_SPEED,
    WeatherEntity,
    WeatherEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    LENGTH_KILOMETERS,
    LENGTH_MILLIMETERS,
    PRESSURE_HPA,
    PRESSURE_INHG,
    SPEED_METERS_PER_SECOND,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.util.pressure import convert as convert_pressure
from pyweatherbitdata.data import ForecastDetailDescription

from .const import DOMAIN
from .entity import WeatherbitEntity
from .models import WeatherBitEntryData

_WEATHER_DAILY = "weather_daily"

WEATHER_TYPES: tuple[WeatherEntityDescription, ...] = (
    WeatherEntityDescription(
        key=_WEATHER_DAILY,
        name="Weatherbit",
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Add a weather entity from a config_entry."""
    entry_data: WeatherBitEntryData = hass.data[DOMAIN][entry.entry_id]
    weatherbitapi = entry_data.weatherbitapi
    coordinator = entry_data.coordinator
    forecast_coordinator = entry_data.forecast_coordinator
    station_data = entry_data.station_data

    entities = []
    for description in WEATHER_TYPES:
        entities.append(
            WeatherbitWeatherEntity(
                weatherbitapi,
                coordinator,
                forecast_coordinator,
                station_data,
                description,
                entry,
                hass.config.units.is_metric,
            )
        )

        _LOGGER.debug(
            "Adding weather entity %s",
            description.name,
        )

    async_add_entities(entities)


class WeatherbitWeatherEntity(WeatherbitEntity, WeatherEntity):
    """A WeatherBit weather entity."""

    def __init__(
        self,
        weatherbitapi,
        coordinator,
        forecast_coordinator,
        station_data,
        description,
        entries: ConfigEntry,
        is_metric: bool,
    ):
        """Initialize an WeatherBit Weather Entity."""
        super().__init__(
            weatherbitapi,
            coordinator,
            forecast_coordinator,
            station_data,
            description,
            entries,
        )
        self.daily_forecast = self.entity_description.key in _WEATHER_DAILY
        self._is_metric = is_metric
        self._attr_name = f"{self.entity_description.name}"

    @property
    def condition(self):
        """Return the current condition."""
        return self.forecast_coordinator.data.condition

    @property
    def temperature(self):
        """Return the temperature."""
        return self.forecast_coordinator.data.temp

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def humidity(self):
        """Return the humidity."""
        return self.forecast_coordinator.data.humidity

    @property
    def precipitation_unit(self) -> str | None:
        return LENGTH_MILLIMETERS

    @property
    def pressure(self):
        """Return the pressure."""
        pressure_hpa = self.forecast_coordinator.data.slp
        if self._is_metric or pressure_hpa is None:
            return pressure_hpa

        return round(convert_pressure(pressure_hpa, PRESSURE_HPA, PRESSURE_INHG), 2)

    @property
    def wind_speed(self):
        """Return the wind speed."""
        if self.forecast_coordinator.data.wind_spd is None:
            return None

        return self.forecast_coordinator.data.wind_spd

    @property
    def wind_speed_unit(self) -> str | None:
        return SPEED_METERS_PER_SECOND

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return self.forecast_coordinator.data.wind_dir

    @property
    def visibility(self):
        """Return the visibility."""
        return self.forecast_coordinator.data.vis

    @property
    def visibility_unit(self) -> str | None:
        return LENGTH_KILOMETERS

    @property
    def ozone(self):
        """Return the ozone."""
        return self.forecast_coordinator.data.ozone

    @property
    def forecast(self):
        """Return the forecast array."""
        data = []
        if self.daily_forecast:
            forecast_data: ForecastDetailDescription = (
                self.forecast_coordinator.data.forecast
            )
            for item in forecast_data:
                data.append(
                    {
                        ATTR_FORECAST_TIME: item.utc_time,
                        ATTR_FORECAST_TEMP: item.max_temp,
                        ATTR_FORECAST_TEMP_LOW: item.min_temp,
                        ATTR_FORECAST_PRECIPITATION: item.precip,
                        ATTR_FORECAST_PRECIPITATION_PROBABILITY: item.pop,
                        ATTR_FORECAST_CONDITION: item.condition,
                        ATTR_FORECAST_WIND_SPEED: item.wind_spd,
                        ATTR_FORECAST_WIND_BEARING: item.wind_dir,
                    }
                )
            return data

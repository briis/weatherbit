"""Support for the Weatherbit weather service."""
from __future__ import annotations

import logging

from homeassistant.components.weather import (
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
    WeatherEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PRECISION_TENTHS,
    UnitOfLength,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from pyweatherbitdata.data import ForecastDetailDescription

from .const import ATTR_ALT_CONDITION, DOMAIN
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
            )
        )

        _LOGGER.debug(
            "Adding weather entity %s",
            description.name,
        )

    async_add_entities(entities)


class WeatherbitWeatherEntity(WeatherbitEntity, WeatherEntity):
    """A WeatherBit weather entity."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Seven is reasonable in this case.

    _attr_has_entity_name = True
    _attr_native_precipitation_unit = UnitOfLength.MILLIMETERS
    _attr_precision = PRECISION_TENTHS
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY
    )

    def __init__(
        self,
        weatherbitapi,
        coordinator,
        forecast_coordinator,
        station_data,
        description,
        entries: ConfigEntry,
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
        self._attr_name = self.entity_description.name

    @property
    def condition(self):
        """Return the current condition."""
        return getattr(self.forecast_coordinator.data, "condition")

    @property
    def native_temperature(self):
        """Return the temperature."""
        return getattr(self.coordinator.data, "temp")

    @property
    def humidity(self):
        """Return the humidity."""
        return getattr(self.coordinator.data, "humidity")

    @property
    def native_pressure(self):
        """Return the pressure."""
        if getattr(self.coordinator.data, "slp") is None:
            return None

        return getattr(self.coordinator.data, "slp")

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        if getattr(self.coordinator.data, "wind_spd") is None:
            return None

        return getattr(self.coordinator.data, "wind_spd")

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return getattr(self.coordinator.data, "wind_dir")

    @property
    def native_visibility(self):
        """Return the visibility."""
        return getattr(self.coordinator.data, "vis")

    @property
    def ozone(self):
        """Return the ozone."""
        return getattr(self.forecast_coordinator.data, "ozone")

    @property
    def extra_state_attributes(self):
        """Return extra state attributes"""
        return {
            **super().extra_state_attributes,
            ATTR_ALT_CONDITION: getattr(
                self.forecast_coordinator.data, "alt_condition"
            ),
        }

    def _forecast(self, hourly: bool) -> list[Forecast] | None:
        """Return the forecast array."""
        data: list[Forecast] = []

        _LOGGER.debug("Getting forecast data")

        if not hourly:
            if self.daily_forecast:
                forecast_data: ForecastDetailDescription = (
                    self.forecast_coordinator.data.forecast
                )
                for item in forecast_data:
                    data.append(
                        {
                            "condition": item.condition,
                            "datetime": item.utc_time,
                            "precipitation_probability": item.pop,
                            "native_precipitation": item.precip,
                            "native_temperature": item.max_temp,
                            "native_templow": item.min_temp,
                            "wind_bearing": item.wind_dir,
                            "native_wind_speed": item.wind_spd,
                        }
                    )
        return data


    # @property
    # def forecast(self) -> list[Forecast] | None:
    #     """Return the forecast array."""
    #     data: list[Forecast] = []
    #     if self.daily_forecast:
    #         forecast_data: ForecastDetailDescription = (
    #             self.forecast_coordinator.data.forecast
    #         )
    #         for item in forecast_data:
    #             data.append(
    #                 {
    #                     ATTR_FORECAST_TIME: item.utc_time,
    #                     ATTR_FORECAST_NATIVE_TEMP: item.max_temp,
    #                     ATTR_FORECAST_NATIVE_TEMP_LOW: item.min_temp,
    #                     ATTR_FORECAST_NATIVE_PRECIPITATION: item.precip,
    #                     ATTR_FORECAST_PRECIPITATION_PROBABILITY: item.pop,
    #                     ATTR_FORECAST_CONDITION: item.condition,
    #                     ATTR_FORECAST_NATIVE_WIND_SPEED: item.wind_spd,
    #                     ATTR_FORECAST_WIND_BEARING: item.wind_dir,
    #                 }
    #             )
    #         return data
    #     return data

    @callback
    def _async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast in native units."""
        return self._forecast(False)

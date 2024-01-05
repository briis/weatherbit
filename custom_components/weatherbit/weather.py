"""Support for the Weatherbit weather service."""
from __future__ import annotations

import logging

from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from homeassistant.components.weather import (
    DOMAIN as WEATHER_DOMAIN,
    Forecast,
    SingleCoordinatorWeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    PRECISION_TENTHS,
    UnitOfLength,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.unit_system import METRIC_SYSTEM
from homeassistant.util.dt import utc_from_timestamp

from . import WeatherbitForecastDataUpdateCoordinator

from pyweatherbitdata.data import ForecastDetailDescription

from .const import ATTR_ALT_CONDITION, DEFAULT_ATTRIBUTION, DEFAULT_BRAND, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add a weather entity from a config_entry."""

    coordinator: WeatherbitForecastDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entity_registry = er.async_get(hass)

    name: str = "weather_daily"
    is_metric = hass.config.units is METRIC_SYSTEM

    entities = [WeatherbitWeather(coordinator, config_entry.data,
                                   False, name, is_metric)]

    async_add_entities(entities)

    # entry_data: WeatherBitEntryData = hass.data[DOMAIN][config_entry.entry_id]
    # weatherbitapi = entry_data.weatherbitapi
    # coordinator: WeatherbitForecastDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    # forecast_coordinator = entry_data.forecast_coordinator
    # station_data = entry_data.station_data

    # entities = [WeatherbitWeather(coordinator, config_entry.data,
    #                                False, name, is_metric)]

    # async_add_entities(entities)

def _calculate_unique_id(config: MappingProxyType[str, Any], hourly: bool) -> str:
    """Calculate unique ID."""
    name_appendix = ""
    if hourly:
        name_appendix = "-hourly"

    return f"{config[CONF_LATITUDE]}_{config[CONF_LONGITUDE]}_{name_appendix}"

class WeatherbitWeather(SingleCoordinatorWeatherEntity[WeatherbitForecastDataUpdateCoordinator]):
    """Implementation of a Weatherbit weather condition."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # Seven is reasonable in this case.

    _attr_attribution = (
        ATTR_ATTRIBUTION
    )
    _attr_has_entity_name = True
    _attr_native_precipitation_unit = UnitOfLength.MILLIMETERS
    _attr_precision = PRECISION_TENTHS
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY
    )

    def __init__(
        self,
        coordinator: WeatherbitForecastDataUpdateCoordinator,
        config: MappingProxyType[str, Any],
        hourly: bool,
        name: str,
        is_metric: bool,
    ):
        """Initialize an WeatherBit Weather Entity."""
        super().__init__(coordinator)

        self._attr_unique_id = _calculate_unique_id(config, hourly)
        self._attr_name = name
        self._config = config
        self._is_metric = is_metric
        self._hourly = hourly
        self._attr_entity_registry_enabled_default = not hourly
        self._attr_device_info = DeviceInfo(
            manufacturer=DEFAULT_BRAND,
            via_device=(DOMAIN, self._attr_unique_id),
            connections={(dr.CONNECTION_NETWORK_MAC, self._attr_unique_id)},
            configuration_url="https://www.weatherbit.io/",
        )

    @property
    def condition(self):
        """Return the current condition."""
        return getattr(self.coordinator.data.daily_forecast, "condition")

    @property
    def native_temperature(self):
        """Return the temperature."""
        return getattr(self.coordinator.data.current_weather_data, "temp")

    @property
    def humidity(self):
        """Return the humidity."""
        return getattr(self.coordinator.data.current_weather_data, "humidity")

    @property
    def native_pressure(self):
        """Return the pressure."""
        if getattr(self.coordinator.data.current_weather_data, "slp") is None:
            return None

        return getattr(self.coordinator.data.current_weather_data, "slp")

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        if getattr(self.coordinator.data.current_weather_data, "wind_spd") is None:
            return None

        return getattr(self.coordinator.data.current_weather_data, "wind_spd")

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return getattr(self.coordinator.data.current_weather_data, "wind_dir")

    @property
    def native_visibility(self):
        """Return the visibility."""
        return getattr(self.coordinator.data.current_weather_data, "vis")

    @property
    def ozone(self):
        """Return the ozone."""
        return getattr(self.coordinator.data.daily_forecast.ozone, "ozone")

    @property
    def extra_state_attributes(self):
        """Return extra state attributes"""
        return {
            **super().extra_state_attributes,
            ATTR_ALT_CONDITION: getattr(
                self.coordinator.data.current_weather_data, "alt_condition"
            ),
        }

    def _forecast(self, hourly: bool) -> list[Forecast] | None:
        """Return the forecast array."""
        data: list[Forecast] = []

        _LOGGER.debug("Getting forecast data")

        if not hourly:
            for item in self.coordinator.data.daily_forecast.forecast:
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

            # if self.daily_forecast:
            #     forecast_data: ForecastDetailDescription = (
            #         self.coordinator.data.daily_forecast.forecast
            #     )
            #     for item in forecast_data:
            #         data.append(
            #             {
            #                 "condition": item.condition,
            #                 "datetime": item.utc_time,
            #                 "precipitation_probability": item.pop,
            #                 "native_precipitation": item.precip,
            #                 "native_temperature": item.max_temp,
            #                 "native_templow": item.min_temp,
            #                 "wind_bearing": item.wind_dir,
            #                 "native_wind_speed": item.wind_spd,
            #             }
            #         )
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

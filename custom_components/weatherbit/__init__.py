"""Support for the Weatherbit weather service."""
from __future__ import annotations

from datetime import timedelta
import logging
from types import MappingProxyType
from typing import Any, Self

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ConfigEntryNotReady, Unauthorized
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from homeassistant.const import (
    CONF_ID,
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
from homeassistant.util.unit_system import (
    METRIC_SYSTEM,
)

from pyweatherbitdata import (
    RequestError,
    InvalidApiKey,
    ResultError,
    WeatherBitApiClient,
)
from pyweatherbitdata.data import (
    BaseDataDescription,
    ForecastDescription,
    ObservationDescription,
)

from .const import (
    DEFAULT_INTERVAL_FORECAST,
    DEFAULT_INTERVAL_SENSORS,
    DOMAIN,
    CONF_FORECAST_LANGUAGE,
    CONF_INTERVAL_FORECAST,
    CONF_INTERVAL_SENSORS,
    CONF_UNIT_SYSTEM_IMPERIAL,
    CONF_UNIT_SYSTEM_METRIC,
    CONFIG_OPTIONS,
    DEFAULT_BRAND,
    WEATHERBIT_API_VERSION,
    WEATHERBIT_PLATFORMS,
)
#from .models import WeatherBitEntryData

#PLATFORMS = [Platform.WEATHER, Platform.SENSOR]
PLATFORMS = [Platform.WEATHER]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Weatherbit Forecast as config entry."""

    coordinator = WeatherbitForecastDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    config_entry.async_on_unload(config_entry.add_update_listener(async_update_entry))

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok

async def async_update_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Reload WeatherFlow Forecast component when options changed."""
    await hass.config_entries.async_reload(config_entry.entry_id)



class CannotConnect(HomeAssistantError):
    """Unable to connect to the web site."""


class WeatherbitForecastDataUpdateCoordinator(DataUpdateCoordinator["WeatherbitForecastWeatherData"]):
    """Class to manage fetching Weatherbit data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize global Weatherbit forecast data updater."""
        self.weather = WeatherbitForecastWeatherData(hass, config_entry)
        self.weather.initialize_data()
        self.hass = hass
        self.config_entry = config_entry

        update_interval=timedelta(minutes=self.config_entry.options.get(CONF_INTERVAL_SENSORS, DEFAULT_INTERVAL_SENSORS)),

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self) -> WeatherbitForecastWeatherData:
        """Fetch data from Weatherbit Forecast."""
        try:
            return await self.weather.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Update failed: {err}") from err


class WeatherbitForecastWeatherData:
    """Keep data for Weatherbit Forecast entity data."""

    def __init__(self, hass: HomeAssistant, config: MappingProxyType[str, Any]) -> None:
        """Initialise the weather entity data."""
        self.hass = hass
        self._config = config
        self._weather_data: WeatherBitApiClient
        self.current_weather_data: ObservationDescription = {}
        self.daily_forecast: ForecastDescription = []
        self.station_data: BaseDataDescription = {}

    def initialize_data(self) -> bool:
        """Establish connection to API."""

        unit_system = (
            CONF_UNIT_SYSTEM_METRIC
            if self.hass.config.units is METRIC_SYSTEM
            else CONF_UNIT_SYSTEM_IMPERIAL
        )

        self._weather_data = WeatherBitApiClient(
            self._config.data[CONF_API_KEY], self._config.data[CONF_LATITUDE], self._config.data[CONF_LONGITUDE], units=unit_system, language=self._config.options[CONF_FORECAST_LANGUAGE], homeassistant=True, session=async_get_clientsession(self.hass))


        return True

    async def fetch_data(self) -> Self:
        """Fetch data from API - (current weather and forecast)."""

        await self._weather_data.initialize()
        self.station_data = self._weather_data.station_data

        # Update Forecast Data
        try:
            resp: ForecastDescription = await self._weather_data.update_forecast()
        except InvalidApiKey as unauthorized:
            _LOGGER.debug(unauthorized)
            raise Unauthorized from unauthorized
        except RequestError as err:
            _LOGGER.debug(err)
            return False
        except ResultError as notreadyerror:
            _LOGGER.debug(notreadyerror)
            raise ConfigEntryNotReady from notreadyerror

        if not resp:
            raise CannotConnect()
        self.current_weather_data = resp
        self.daily_forecast = resp

        # Update Observation Data
        try:
            resp: ObservationDescription = await self._weather_data.update_sensors()
        except InvalidApiKey as unauthorized:
            _LOGGER.debug(unauthorized)
            raise Unauthorized from unauthorized
        except RequestError as err:
            _LOGGER.debug(err)
            return False
        except ResultError as notreadyerror:
            _LOGGER.debug(notreadyerror)
            raise ConfigEntryNotReady from notreadyerror

        if not resp:
            raise CannotConnect()
        self.current_weather_data = resp


        return self




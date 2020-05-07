"""Support for the Weatherbit weather service."""
import asyncio
from datetime import timedelta
import logging
from typing import Dict, List

import aiohttp
import async_timeout
from weatherbitpypi import Api, WeatherbitError

from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    WeatherEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    CONF_API_KEY,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.util import Throttle, slugify

from .const import ATTR_WEATHERBIT_CLOUDINESS, ENTITY_ID_SENSOR_FORMAT

_LOGGER = logging.getLogger(__name__)

# Used to map condition from API results
CONDITION_CLASSES = {
    "cloudy": [804, 803],
    "fog": [741],
    "hail": [623],
    "lightning": [230, 231],
    "lightning-rainy": [200, 201, 202],
    "partlycloudy": [801, 802],
    "pouring": [502, 522],
    "rainy": [300, 301, 302, 500, 501, 511, 520, 521],
    "snowy": [600, 601, 602, 621, 622, 623],
    "snowy-rainy": [610, 611, 612],
    "sunny": [800, 801, 802],
    "windy": [],
    "windy-variant": [],
    "exceptional": [],
}

# 5 minutes between retrying connect to API again
RETRY_TIMEOUT = 5 * 60

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, config_entries
) -> bool:
    """Add a weather entity from map location."""
    location = config_entry.data
    name = slugify(location[CONF_NAME])

    session = aiohttp_client.async_get_clientsession(hass)

    entity = WeatherbitWeather(
        location[CONF_NAME],
        location[CONF_API_KEY],
        location[CONF_LATITUDE],
        location[CONF_LONGITUDE],
        session,
    )
    entity.entity_id = ENTITY_ID_SENSOR_FORMAT.format(name)

    config_entries([entity], True)
    return True


class WeatherbitWeather(WeatherEntity):
    """Representation of a weather entity."""

    def __init__(
        self,
        name: str,
        api_key: str,
        latitude: str,
        longitude: str,
        session: aiohttp.ClientSession = None,
    ) -> None:
        """Initialize the Weatherbit weather entity."""

        self._name = name
        self._api_key = api_key
        self._latitude = latitude
        self._longitude = longitude
        self._forecasts = None
        self._fail_count = 0
        self._api = Api(
            self._api_key, self._latitude, self._longitude, "en", "M", session=session
        )

    @property
    def unique_id(self) -> str:
        """Return a unique id."""
        return f"{self._latitude}, {self._longitude}"

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Refresh the forecast data from SMHI weather API."""
        try:
            with async_timeout.timeout(10):
                self._forecasts = await self.get_weather_forecast()
                self._fail_count = 0
                _LOGGER.debug("Weatherbit Forecast Updated")

        except (asyncio.TimeoutError, WeatherbitError):
            _LOGGER.error("Failed to connect to Weatherbit API, retry in 5 minutes")
            self._fail_count += 1
            if self._fail_count < 3:
                self.hass.helpers.event.async_call_later(
                    RETRY_TIMEOUT, self.retry_update
                )

    async def retry_update(self, _):
        """Retry refresh weather forecast."""
        await self.async_update()

    async def get_weather_forecast(self) -> []:
        """Return the current forecasts from SMHI API."""
        return await self._api.async_get_forecast_daily()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def temperature(self) -> int:
        """Return the temperature."""
        if self._forecasts is not None:
            return self._forecasts[0].temp
        return None

    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def humidity(self) -> int:
        """Return the humidity."""
        if self._forecasts is not None:
            return self._forecasts[0].humidity
        return None

    @property
    def wind_speed(self) -> float:
        """Return the wind speed."""
        if self._forecasts is not None:
            # Convert from m/s to km/h
            return round(self._forecasts[0].wind_spd * 18 / 5)
        return None

    @property
    def wind_bearing(self) -> int:
        """Return the wind bearing."""
        if self._forecasts is not None:
            return self._forecasts[0].wind_dir
        return None

    @property
    def visibility(self) -> float:
        """Return the visibility."""
        if self._forecasts is not None:
            return self._forecasts[0].vis
        return None

    @property
    def pressure(self) -> int:
        """Return the pressure."""
        if self._forecasts is not None:
            return self._forecasts[0].pres
        return None

    @property
    def cloudiness(self) -> int:
        """Return the cloudiness."""
        if self._forecasts is not None:
            return self._forecasts[0].clouds
        return None

    @property
    def condition(self) -> str:
        """Return the weather condition."""
        if self._forecasts is None:
            return None
        return next(
            (
                k
                for k, v in CONDITION_CLASSES.items()
                if self._forecasts[0].weather_code in v
            ),
            None,
        )

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return "Weatherbit"

    @property
    def forecast(self) -> List:
        """Return the forecast."""
        if self._forecasts is None or len(self._forecasts) < 2:
            return None

        data = []

        for forecast in self._forecasts[1:]:
            condition = next(
                (k for k, v in CONDITION_CLASSES.items() if forecast.weather_code in v),
                None,
            )

            data.append(
                {
                    ATTR_FORECAST_TIME: forecast.valid_date,
                    ATTR_FORECAST_TEMP: forecast.max_temp,
                    ATTR_FORECAST_TEMP_LOW: forecast.min_temp,
                    ATTR_FORECAST_PRECIPITATION: round(forecast.precip, 1),
                    ATTR_FORECAST_CONDITION: condition,
                }
            )

        return data

    @property
    def device_state_attributes(self) -> Dict:
        """Return SMHI specific attributes."""
        if self.cloudiness:
            return {ATTR_WEATHERBIT_CLOUDINESS: self.cloudiness}

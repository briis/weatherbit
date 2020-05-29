"""Support for the Weatherbit weather service."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from weatherbitpypi import Weatherbit, WeatherbitError

from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import homeassistant.helpers.device_registry as dr
from homeassistant.const import (
    CONF_ID,
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)

from .const import (
    DOMAIN,
    CONF_CUR_UPDATE_INTERVAL,
    CONF_FCS_UPDATE_INTERVAL,
    DEFAULT_BRAND,
    DEFAULT_SCAN_INTERVAL,
    WEATHERBIT_PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up configured Weatherbit."""
    # We allow setup only through config flow type of config
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up Weatherbit forecast as config entry."""
    session = aiohttp_client.async_get_clientsession(hass)

    weatherbit = Weatherbit(
        entry.data[CONF_API_KEY],
        entry.data[CONF_LATITUDE],
        entry.data[CONF_LONGITUDE],
        "en",
        "M",
        session,
    )
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = weatherbit
    _LOGGER.debug("Connected to Weatherbit")

    if entry.data.get(CONF_FCS_UPDATE_INTERVAL):
        fcst_scan_interval = timedelta(minutes=entry.data[CONF_FCS_UPDATE_INTERVAL])
    else:
        fcst_scan_interval = SCAN_INTERVAL

    fcst_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=weatherbit.async_get_forecast_daily,
        update_interval=fcst_scan_interval,
    )

    if entry.data.get(CONF_CUR_UPDATE_INTERVAL):
        current_scan_interval = timedelta(minutes=entry.data[CONF_CUR_UPDATE_INTERVAL])
    else:
        current_scan_interval = SCAN_INTERVAL

    cur_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=weatherbit.async_get_current_data,
        update_interval=current_scan_interval,
    )

    await fcst_coordinator.async_refresh()
    await cur_coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "fcst_coordinator": fcst_coordinator,
        "cur_coordinator": cur_coordinator,
        "weatherbit": weatherbit,
    }

    await _async_get_or_create_weatherbit_device_in_registry(hass, entry)

    for platform in WEATHERBIT_PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def _async_get_or_create_weatherbit_device_in_registry(
    hass: HomeAssistantType, entry: ConfigEntry
) -> None:
    device_registry = await dr.async_get_registry(hass)
    device_key = f"{entry.data[CONF_LATITUDE]}_{entry.data[CONF_LONGITUDE]}"
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, device_key)},
        identifiers={(DOMAIN, device_key)},
        manufacturer=DEFAULT_BRAND,
        name=entry.data[CONF_ID],
        model="Current and Forecast Weather Data",
    )


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Unload Unifi Protect config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in WEATHERBIT_PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

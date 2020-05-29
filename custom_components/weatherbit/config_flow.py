"""Config flow to configure Weatherbit component."""
import logging

from weatherbitpypi import Weatherbit, WeatherbitError

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_API_KEY,
    CONF_ID,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
from homeassistant.config_entries import ConfigFlow
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    CONF_ADD_SENSORS,
    CONF_CUR_UPDATE_INTERVAL,
    CONF_FCS_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class WeatherbitFlowHandler(ConfigFlow):
    """Config flow for Weatherbit component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(
                        CONF_LATITUDE, default=self.hass.config.latitude
                    ): cv.latitude,
                    vol.Required(
                        CONF_LONGITUDE, default=self.hass.config.longitude
                    ): cv.longitude,
                    vol.Optional(
                        CONF_FCS_UPDATE_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=30, max=120)),
                    vol.Optional(
                        CONF_CUR_UPDATE_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=4, max=60)),
                    vol.Optional(CONF_ADD_SENSORS, default=True): bool,
                }
            ),
            errors=errors or {},
        )

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        errors = {}

        wbit_client = Weatherbit(
            user_input[CONF_API_KEY],
            user_input[CONF_LATITUDE],
            user_input[CONF_LONGITUDE],
        )

        try:
            unique_id = await wbit_client.async_get_city_name()
        except WeatherbitError:
            errors["base"] = "connection_error"
            return await self._show_setup_form(errors)

        entries = self._async_current_entries()
        for entry in entries:
            if entry.data[CONF_ID] == unique_id:
                return self.async_abort(reason="name_exists")

        return self.async_create_entry(
            title=unique_id,
            data={
                CONF_ID: unique_id,
                CONF_API_KEY: user_input[CONF_API_KEY],
                CONF_LATITUDE: user_input[CONF_LATITUDE],
                CONF_LONGITUDE: user_input.get(CONF_LONGITUDE),
                CONF_FCS_UPDATE_INTERVAL: user_input.get(CONF_FCS_UPDATE_INTERVAL),
                CONF_CUR_UPDATE_INTERVAL: user_input.get(CONF_CUR_UPDATE_INTERVAL),
                CONF_ADD_SENSORS: user_input.get(CONF_ADD_SENSORS),
            },
        )

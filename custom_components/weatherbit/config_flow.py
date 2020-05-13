"""Config flow to configure Weatherbit component."""
from weatherbitpypi import Weatherbit, WeatherbitError

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME, CONF_API_KEY
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client
import homeassistant.helpers.config_validation as cv
from homeassistant.util import slugify

from .const import DOMAIN, HOME_LOCATION_NAME


@callback
def weatherbit_locations(hass: HomeAssistant):
    """Return configurations of Weatherbit component."""
    return {
        (slugify(entry.data[CONF_NAME]))
        for entry in hass.config_entries.async_entries(DOMAIN)
    }


@config_entries.HANDLERS.register(DOMAIN)
class WeatherbitFlowHandler(config_entries.ConfigFlow):
    """Config flow for Weatherbit component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Initialize Weatherbit forecast configuration flow."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            is_ok = await self._check_location(
                user_input[CONF_API_KEY],
                user_input[CONF_LONGITUDE],
                user_input[CONF_LATITUDE],
            )
            if is_ok:
                name = slugify(user_input[CONF_NAME])
                if not self._name_in_configuration_exists(name):
                    return self.async_create_entry(
                        title=user_input[CONF_NAME], data=user_input
                    )

                self._errors[CONF_NAME] = "name_exists"
            else:
                self._errors["base"] = "wrong_location"

        # If hass config has the location set and is a valid coordinate the
        # default location is set as default values in the form
        if not weatherbit_locations(self.hass):
            if await self._homeassistant_location_exists():
                return await self._show_config_form(
                    name=HOME_LOCATION_NAME,
                    latitude=self.hass.config.latitude,
                    longitude=self.hass.config.longitude,
                )

        return await self._show_config_form()

    async def _homeassistant_location_exists(self) -> bool:
        """Return true if default location is set and is valid."""
        if self.hass.config.latitude != 0.0 and self.hass.config.longitude != 0.0:
            return True
        else:
            return False

    def _name_in_configuration_exists(self, name: str) -> bool:
        """Return True if name exists in configuration."""
        if name in weatherbit_locations(self.hass):
            return True
        return False

    async def _show_config_form(
        self, name: str = None, latitude: str = None, longitude: str = None
    ):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=name): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_LATITUDE, default=latitude): cv.latitude,
                    vol.Required(CONF_LONGITUDE, default=longitude): cv.longitude,
                }
            ),
            errors=self._errors,
        )

    async def _check_location(
        self, api_key: str, longitude: str, latitude: str
    ) -> bool:
        """Return true if location is ok."""

        try:
            # session = aiohttp_client.async_get_clientsession(self.hass)
            wbit_api = Weatherbit(api_key, latitude, longitude)

            await wbit_api.async_get_current_data()

            return True
        except WeatherbitError:
            # The API will throw an exception if faulty location
            pass

        return False

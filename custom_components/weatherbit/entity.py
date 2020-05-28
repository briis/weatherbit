"""Base Entity for Weatherbit."""

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.device_registry as dr

from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
from .const import (
    DOMAIN,
    DEFAULT_BRAND,
    DEFAULT_ATTRIBUTION,
)


class WeatherbitEntity(Entity):
    """Base class for Weatherbit Entities."""

    def __init__(self, fcst_coordinator, cur_coordinator, entries):
        """Initialize the Weatherbit Entity."""
        super().__init__()
        self.fcst_coordinator = fcst_coordinator
        self.cur_coordinator = cur_coordinator
        self.entries = entries
        self._device_key = (
            f"{self.entries[CONF_LATITUDE]}_{self.entries[CONF_LONGITUDE]}"
        )

    @property
    def _forecast(self):
        return self.fcst_coordinator.data[0]

    @property
    def _current(self):
        return self.cur_coordinator.data[0]

    @property
    def device_info(self):
        return {
            "connections": {(dr.CONNECTION_NETWORK_MAC, self._device_key)},
            "manufacturer": DEFAULT_BRAND,
            "model": "Current and Forecast Weather Data",
            "via_device": (DOMAIN, self._device_key),
        }

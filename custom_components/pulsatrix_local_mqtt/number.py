"""The pulsatrix (MQTT) number entities for setting limits."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.number import NumberEntity, NumberMode

from .definitions.number import NUMBERS, PxChargerNumberEntityDescription
from .entity import PxChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: core.HomeAssistant,
        config_entry: config_entries.ConfigEntry,
        async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        PxChargerNumber(config_entry, description)
        for description in NUMBERS
        if not description.disabled
    )


class PxChargerNumber(PxChargerEntity, NumberEntity):
    """Representation of a pulsatrix number entity for setting limits via MQTT."""

    entity_description: PxChargerNumberEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: PxChargerNumberEntityDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(config_entry, description)

        self.entity_description = description
        self._attr_native_value = description.native_value
        self._attr_native_min_value = description.native_min_value
        self._attr_native_max_value = description.native_max_value
        self._attr_native_step = description.native_step
        self._attr_mode = description.mode

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        if self.entity_description.value_formatter:
            payload = self.entity_description.value_formatter(value)
        else:
            payload = str(value)

        await mqtt.async_publish(self.hass, self._topic, payload)
        self._attr_native_value = value
        self.async_write_ha_state()

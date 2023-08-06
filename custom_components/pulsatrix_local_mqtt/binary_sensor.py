"""The pulsatrix (MQTT) binary sensor."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import callback

from .definitions.binary_sensor import (
    BINARY_SENSORS,
    PxChargerBinarySensorEntityDescription,
)
from .entity import PxChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        PxChargerBinarySensor(config_entry, description)
        for description in BINARY_SENSORS
        if not description.disabled
    )


class PxChargerBinarySensor(PxChargerEntity, BinarySensorEntity):
    """Representation of a pulsatrix sensor that is updated via MQTT."""

    entity_description: PxChargerBinarySensorEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: PxChargerBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        self.entity_description = description

        super().__init__(config_entry, description)

    @property
    def available(self):
        """Return True if entity is available."""
        return self._attr_is_on is not None

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_is_on = self.entity_description.state(
                    message.payload, self.entity_description.attribute
                )
            else:
                if message.payload == "true":
                    self._attr_is_on = True
                elif message.payload == "false":
                    self._attr_is_on = False
                else:
                    self._attr_is_on = None

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)

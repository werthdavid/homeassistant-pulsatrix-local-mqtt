"""The pulsatrix (MQTT) sensor."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback

from .definitions.sensor import SENSORS, PxChargerSensorEntityDescription
from .entity import PxChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: core.HomeAssistant,
        config_entry: config_entries.ConfigEntry,
        async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        PxChargerSensor(config_entry, description)
        for description in SENSORS
        if not description.disabled
    )


class PxChargerSensor(PxChargerEntity, SensorEntity):
    """Representation of a pulsatrix sensor that is updated via MQTT."""

    entity_description: PxChargerSensorEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: PxChargerSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self._extra_state_attributes = None
        self.entity_description = description

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._extra_state_attributes

    @property
    def available(self):
        if self.entity_description.initial_value is not None:
            return True
        """Return True if entity is available."""
        return self._attr_native_value is not None

    async def async_added_to_hass(self):
        if self.entity_description.initial_value is not None:
            self._attr_native_value = self.entity_description.initial_value

        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_native_value = self.entity_description.state(
                    message.payload, self.entity_description.attribute, self.entity_description.attribute_index
                )
            else:
                if message.payload == "null":
                    self._attr_native_value = None
                else:
                    self._attr_native_value = message.payload

            if self.entity_description.raw_value is not None:
                raw_value = self.entity_description.raw_value(
                    message.payload, self.entity_description.attribute, self.entity_description.attribute_index
                )
                self._extra_state_attributes = {
                    "raw_value": raw_value
                }

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)

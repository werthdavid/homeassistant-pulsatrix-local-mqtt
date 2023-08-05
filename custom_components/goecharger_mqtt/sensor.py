"""The go-eCharger (MQTT) sensor."""
import logging

from homeassistant import config_entries, core
from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback

from .definitions.sensor import SENSORS, GoEChargerSensorEntityDescription
from .entity import GoEChargerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        GoEChargerSensor(config_entry, description)
        for description in SENSORS
        if not description.disabled
    )


class GoEChargerSensor(GoEChargerEntity, SensorEntity):
    """Representation of a go-eCharger sensor that is updated via MQTT."""

    entity_description: GoEChargerSensorEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: GoEChargerSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self.entity_description = description

    @property
    def available(self):
        """Return True if entity is available."""
        return self._attr_native_value is not None

    async def async_added_to_hass(self):
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if self.entity_description.state is not None:
                self._attr_native_value = self.entity_description.state(
                    message.payload, self.entity_description.attribute
                )
            else:
                if message.payload == "null":
                    self._attr_native_value = None
                else:
                    self._attr_native_value = message.payload

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 1)

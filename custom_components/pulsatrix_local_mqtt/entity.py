"""MQTT component mixins and helpers."""
from homeassistant import config_entries
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.util import slugify

from .const import (
    CONF_SERIAL_NUMBER,
    CONF_TOPIC_PREFIX,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MODEL,
    DOMAIN,
)
from .definitions import PxChargerEntityDescription


class PxChargerEntity(Entity):
    """Common pulsatrix entity."""

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: PxChargerEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        topic_prefix = config_entry.data[CONF_TOPIC_PREFIX]
        serial_number = config_entry.data[CONF_SERIAL_NUMBER]

        self._topic = f"{topic_prefix}/{serial_number}/{description.topic}"
        self.entity_id = f"{description.domain}.pulsatrix_{serial_number}_{description.key}"

        self._attr_unique_id = "-".join(
            [serial_number, description.domain, description.key]
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            name=config_entry.title,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
        )

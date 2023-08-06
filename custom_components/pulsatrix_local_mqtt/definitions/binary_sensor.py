"""Definitions for pulsatrix binary sensors exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import json
import logging

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.helpers.entity import EntityCategory

from . import PxChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class PxChargerBinarySensorEntityDescription(
    PxChargerEntityDescription, BinarySensorEntityDescription
):
    """Binary sensor entity description for pulsatrix."""
    domain: str = "binary_sensor"


def map_state_to_boolean(value, key) -> bool:
    return json.loads(value)[key] == "CHARGING"


BINARY_SENSORS: tuple[PxChargerBinarySensorEntityDescription, ...] = (
    PxChargerBinarySensorEntityDescription(
        key="charging",
        topic="tx/status",
        name="pulsatrix Charging",
        attribute="state",
        state=map_state_to_boolean,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        icon="mdi:ev-plug-type2",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
)

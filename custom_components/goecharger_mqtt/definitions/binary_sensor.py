"""Definitions for go-eCharger binary sensors exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import json
import logging

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.helpers.entity import EntityCategory

from . import GoEChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class GoEChargerBinarySensorEntityDescription(
    GoEChargerEntityDescription, BinarySensorEntityDescription
):
    """Binary sensor entity description for go-eCharger."""

    domain: str = "binary_sensor"


def map_car_idle_to_bool(value, key) -> bool:
    """Extract item from array to int."""
    return int(value) > int(key)


BINARY_SENSORS: tuple[GoEChargerBinarySensorEntityDescription, ...] = (
    GoEChargerBinarySensorEntityDescription(
        key="car",
        name="Car connected",
        attribute="1",
        state=map_car_idle_to_bool,
        entity_category=EntityCategory.CONFIG,
        device_class=None,
        icon="mdi:car",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
)

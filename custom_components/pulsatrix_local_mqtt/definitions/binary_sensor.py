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


def map_plug_lock_to_boolean(value, key) -> bool | None:
    try:
        return json.loads(value)[key] == True
    except (KeyError, TypeError):
        return None


def map_connector_available(value, key) -> bool:
    return json.loads(value)[key] == "Available"


def map_connector_faulted(value, key) -> bool:
    return json.loads(value)[key] == "Faulted"


def map_vehicle_connected(value, key) -> bool:
    status = json.loads(value)[key]
    return status in ["B", "C", "D"]


BINARY_SENSORS: tuple[PxChargerBinarySensorEntityDescription, ...] = (
    PxChargerBinarySensorEntityDescription(
        key="charging",
        topic="tx/status",
        name="pulsatrix Charging",
        initial_value=False,
        attribute="state",
        state=map_state_to_boolean,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        icon="mdi:ev-plug-type2",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerBinarySensorEntityDescription(
        key="plug_retention_lock",
        topic="charging/status",
        name="pulsatrix Plug Retention Lock",
        attribute="plugRetentionLock",
        state=map_plug_lock_to_boolean,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        icon="mdi:lock",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerBinarySensorEntityDescription(
        key="connector_available",
        topic="chargingPoint/status",
        name="pulsatrix Connector Available",
        initial_value=True,
        attribute="connectorStatus",
        state=map_connector_available,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        icon="mdi:ev-station",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerBinarySensorEntityDescription(
        key="connector_faulted",
        topic="chargingPoint/status",
        name="pulsatrix Connector Faulted",
        initial_value=False,
        attribute="connectorStatus",
        state=map_connector_faulted,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class="problem",
        icon="mdi:alert-circle",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerBinarySensorEntityDescription(
        key="vehicle_connected",
        topic="charging/status",
        name="pulsatrix Vehicle Connected",
        attribute="vehicleStatus",
        state=map_vehicle_connected,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class="plug",
        icon="mdi:car-electric",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
)

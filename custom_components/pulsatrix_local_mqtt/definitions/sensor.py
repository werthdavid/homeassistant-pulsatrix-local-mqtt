"""Definitions for pulsatrix sensors exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import json
import logging

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorDeviceClass,
    SensorEntityDescription,
)
from homeassistant.const import (
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    FREQUENCY_HERTZ,
    POWER_KILO_WATT,
)
from homeassistant.helpers.entity import EntityCategory

from . import PxChargerEntityDescription, PxChargerStatusCodes

_LOGGER = logging.getLogger(__name__)


@dataclass
class PxChargerSensorEntityDescription(
    PxChargerEntityDescription, SensorEntityDescription
):
    """Sensor entity description for pulsatrix."""
    domain: str = "sensor"


def extract_json_float(value, key, index) -> float | None:
    try:
        if index >= 0:
            return round(float(json.loads(value)[key][index]), 2)
        else:
            return round(float(json.loads(value)[key]), 2)
    except IndexError:
        return None


def extract_json_float_kilo(value, key, index) -> float | None:
    try:
        if index >= 0:
            return round(float(json.loads(value)[key][index]) / 1000, 2)
        else:
            return round(float(json.loads(value)[key]) / 1000, 2)
    except IndexError:
        return None


def extract_json_amperage_kilo_watts(value, key, index) -> float | None:
    try:
        if index >= 0:
            return round((float(json.loads(value)[key][index]) * 3 * 238) / 1000, 2)
        else:
            return round((float(json.loads(value)[key]) * 3 * 238) / 1000, 2)
    except IndexError:
        return None


def extract_json(value, key, index) -> str | None:
    try:
        return json.loads(value)[key]
    except IndexError:
        return None


def transform_code(value, key, index) -> str:
    """Transform codes into a human readable string."""
    _LOGGER.debug("transform_code" + json.loads(value)[key])
    try:
        return getattr(PxChargerStatusCodes, "states")[json.loads(value)[key]]
    except KeyError:
        return "Definition missing for code %s" % value


SENSORS: tuple[PxChargerSensorEntityDescription, ...] = (
    PxChargerSensorEntityDescription(
        key="current_consumption",
        topic="meter/fiscal",
        name="pulsatrix Current Consumption",
        state=extract_json_float_kilo,
        attribute="activePower",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=POWER_KILO_WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="effective_amperage_limit",
        topic="tx/status",
        name="pulsatrix Max Consumption",
        state=extract_json_amperage_kilo_watts,
        attribute="effectiveAmperageLimit",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=POWER_KILO_WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="state",
        topic="tx/status",
        name="pulsatrix State",
        state=transform_code,
        raw_value=extract_json,
        attribute="state",
        device_class=None,
        translation_key="i18n_state",
        native_unit_of_measurement=None,
        state_class=None,
        icon="mdi:state-machine",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="frequency",
        topic="meter/fiscal",
        name="pulsatrix Frequency",
        state=extract_json_float,
        attribute="frequency",
        icon="mdi:current-ac",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="p1_voltage",
        topic="meter/fiscal",
        name="pulsatrix P1 voltage",
        state=extract_json_float,
        attribute="voltage",
        attribute_index=0,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="p2_voltage",
        topic="meter/fiscal",
        name="pulsatrix P2 voltage",
        state=extract_json_float,
        attribute="voltage",
        attribute_index=1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="p3_voltage",
        topic="meter/fiscal",
        name="pulsatrix P3 voltage",
        state=extract_json_float,
        attribute="voltage",
        attribute_index=2,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="p1_amperage",
        topic="meter/fiscal",
        name="pulsatrix P1 amperage",
        state=extract_json_float,
        attribute="amperage",
        attribute_index=0,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="p2_amperage",
        topic="meter/fiscal",
        name="pulsatrix P2 amperage",
        state=extract_json_float,
        attribute="amperage",
        attribute_index=1,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="p3_amperage",
        topic="meter/fiscal",
        name="pulsatrix P3 amperage",
        state=extract_json_float,
        attribute="amperage",
        attribute_index=2,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
)

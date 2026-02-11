"""Definitions for pulsatrix sensors exposed via MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import json
import logging
import pytz
from datetime import datetime
from homeassistant.components.sensor import (
    SensorStateClass,
    SensorDeviceClass,
    SensorEntityDescription
)
from homeassistant.const import (
   UnitOfEnergy,UnitOfPower,UnitOfFrequency,UnitOfElectricCurrent,UnitOfElectricPotential,UnitOfTime
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


def extract_energy(value, key, index) -> float | None:
    try:
        return round(float(json.loads(value)["lastMeterValue"]) - float(json.loads(value)["meterStart"]), 2)
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


def transform_connector_status(value, key, index) -> str:
    """Transform connector status codes into a human readable string."""
    try:
        return getattr(PxChargerStatusCodes, "connector_status")[json.loads(value)[key]]
    except KeyError:
        return json.loads(value)[key]


def transform_charge_controller_status(value, key, index) -> str:
    """Transform charge controller status codes into a human readable string."""
    try:
        return getattr(PxChargerStatusCodes, "charge_controller_status")[json.loads(value)[key]]
    except KeyError:
        return json.loads(value)[key]


def transform_vehicle_status(value, key, index) -> str:
    """Transform vehicle status codes into a human readable string."""
    try:
        return getattr(PxChargerStatusCodes, "vehicle_status")[json.loads(value)[key]]
    except KeyError:
        return json.loads(value)[key]


def transform_start_reason(value, key, index) -> str:
    """Transform start reason codes into a human readable string."""
    try:
        return getattr(PxChargerStatusCodes, "start_reason")[json.loads(value)[key]]
    except KeyError:
        return json.loads(value)[key]


def transform_cp_error_cause(value, key, index) -> str:
    """Transform CP error cause codes into a human readable string."""
    try:
        raw = json.loads(value)[key]
        if raw is None or raw == "":
            return None
        return getattr(PxChargerStatusCodes, "cp_error_cause").get(raw, raw)
    except (KeyError, TypeError):
        return None


def map_state_to_datetime(value, key, index) -> str:
    ts = int(json.loads(value)[key])
    if ts == 0:
        return None
    dt = datetime.utcfromtimestamp(ts)
    timezone = pytz.UTC
    return timezone.localize(dt).strftime("%d.%m.%Y %H:%M:%S")


def extract_duration_minutes(value, key, index) -> float | None:
    """Extract charging duration and convert from milliseconds to minutes."""
    try:
        ms = int(json.loads(value)[key])
        return round(ms / 60000, 1)
    except (KeyError, TypeError, ValueError):
        return None


def extract_json_string(value, key, index) -> str | None:
    """Extract a string value from JSON."""
    try:
        return json.loads(value)[key]
    except (KeyError, TypeError):
        return None


def extract_json_bool(value, key, index) -> bool | None:
    """Extract a boolean value from JSON."""
    try:
        return json.loads(value)[key]
    except (KeyError, TypeError):
        return None


SENSORS: tuple[PxChargerSensorEntityDescription, ...] = (
    PxChargerSensorEntityDescription(
        key="current_consumption",
        topic="meter/fiscal",
        name="pulsatrix Current Consumption",
        state=extract_json_float_kilo,
        attribute="activePower",
        initial_value=0,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="energy",
        topic="tx/status",
        name="pulsatrix Energy",
        state=extract_energy,
        attribute="lastMeterValue",
        initial_value=0,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
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
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
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
        initial_value="Idle",
        device_class=None,
        translation_key="i18n_state",
        native_unit_of_measurement=None,
        state_class=None,
        icon="mdi:state-machine",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="started_time",
        topic="tx/status",
        name="pulsatrix Started Time",
        attribute="startedTime",
        state=map_state_to_datetime,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        icon="mdi:car-clock",
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
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        state_class=SensorStateClass.MEASUREMENT,
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
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
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
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
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
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
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
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
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
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
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
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="energy_imported",
        topic="meter/fiscal",
        name="pulsatrix Total Energy Imported",
        state=extract_json_float,
        attribute="energyImported",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    # chargingPoint/status sensors
    PxChargerSensorEntityDescription(
        key="connector_status",
        topic="chargingPoint/status",
        name="pulsatrix Connector Status",
        state=transform_connector_status,
        raw_value=extract_json,
        attribute="connectorStatus",
        initial_value="Available",
        device_class=None,
        translation_key="i18n_connector_status",
        icon="mdi:ev-plug-type2",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    # charging/status sensors
    PxChargerSensorEntityDescription(
        key="charge_controller_status",
        topic="charging/status",
        name="pulsatrix Charge Controller Status",
        state=transform_charge_controller_status,
        raw_value=extract_json,
        attribute="chargeControllerStatus",
        device_class=None,
        translation_key="i18n_charge_controller_status",
        icon="mdi:state-machine",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="vehicle_status",
        topic="charging/status",
        name="pulsatrix Vehicle Status",
        state=transform_vehicle_status,
        raw_value=extract_json,
        attribute="vehicleStatus",
        device_class=None,
        translation_key="i18n_vehicle_status",
        icon="mdi:car-electric",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="available_amperage",
        topic="charging/status",
        name="pulsatrix Available Amperage",
        state=extract_json_float,
        attribute="availableAmperage",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="signaled_amperage",
        topic="charging/status",
        name="pulsatrix Signaled Amperage",
        state=extract_json_float,
        attribute="signaledAmperage",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="charging_duration",
        topic="charging/status",
        name="pulsatrix Charging Duration",
        state=extract_duration_minutes,
        attribute="chargingDuration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:timer",
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="used_phases_session",
        topic="charging/status",
        name="pulsatrix Used Phases",
        state=extract_json_string,
        attribute="usedPhasesSession",
        device_class=None,
        icon="mdi:sine-wave",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="recent_cp_error_cause",
        topic="charging/status",
        name="pulsatrix Recent CP Error Cause",
        state=transform_cp_error_cause,
        raw_value=extract_json,
        attribute="recentCpErrorCause",
        device_class=None,
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    # tx/status sensors (additional)
    PxChargerSensorEntityDescription(
        key="transaction_id",
        topic="tx/status",
        name="pulsatrix Transaction ID",
        state=extract_json_string,
        attribute="id",
        device_class=None,
        icon="mdi:identifier",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="ended_time",
        topic="tx/status",
        name="pulsatrix Ended Time",
        attribute="endedTime",
        state=map_state_to_datetime,
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=None,
        icon="mdi:car-clock",
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="start_reason",
        topic="tx/status",
        name="pulsatrix Start Reason",
        state=transform_start_reason,
        raw_value=extract_json,
        attribute="startReason",
        device_class=None,
        icon="mdi:play-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="energy_active_import_register",
        topic="tx/status",
        name="pulsatrix Energy Active Import Register",
        state=extract_json_float,
        attribute="energyActiveImportRegister",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="last_active_power",
        topic="tx/status",
        name="pulsatrix Last Active Power",
        state=extract_json_float_kilo,
        attribute="lastActivePower",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="meter_start",
        topic="tx/status",
        name="pulsatrix Meter Start",
        state=extract_json_float,
        attribute="meterStart",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="meter_stop",
        topic="tx/status",
        name="pulsatrix Meter Stop",
        state=extract_json_float,
        attribute="meterStop",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="peak_active_power",
        topic="tx/status",
        name="pulsatrix Peak Active Power",
        state=extract_json_float_kilo,
        attribute="peakActivePower",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    # meter/grid sensors
    PxChargerSensorEntityDescription(
        key="grid_power",
        topic="meter/grid",
        name="pulsatrix Grid Power",
        state=extract_json_float_kilo,
        attribute="activePower",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_energy_imported",
        topic="meter/grid",
        name="pulsatrix Grid Energy Imported",
        state=extract_json_float,
        attribute="energyImported",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_frequency",
        topic="meter/grid",
        name="pulsatrix Grid Frequency",
        state=extract_json_float,
        attribute="frequency",
        icon="mdi:current-ac",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_p1_voltage",
        topic="meter/grid",
        name="pulsatrix Grid P1 Voltage",
        state=extract_json_float,
        attribute="voltage",
        attribute_index=0,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_p2_voltage",
        topic="meter/grid",
        name="pulsatrix Grid P2 Voltage",
        state=extract_json_float,
        attribute="voltage",
        attribute_index=1,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_p3_voltage",
        topic="meter/grid",
        name="pulsatrix Grid P3 Voltage",
        state=extract_json_float,
        attribute="voltage",
        attribute_index=2,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_p1_amperage",
        topic="meter/grid",
        name="pulsatrix Grid P1 Amperage",
        state=extract_json_float,
        attribute="amperage",
        attribute_index=0,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_p2_amperage",
        topic="meter/grid",
        name="pulsatrix Grid P2 Amperage",
        state=extract_json_float,
        attribute="amperage",
        attribute_index=1,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
    PxChargerSensorEntityDescription(
        key="grid_p3_amperage",
        topic="meter/grid",
        name="pulsatrix Grid P3 Amperage",
        state=extract_json_float,
        attribute="amperage",
        attribute_index=2,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
)

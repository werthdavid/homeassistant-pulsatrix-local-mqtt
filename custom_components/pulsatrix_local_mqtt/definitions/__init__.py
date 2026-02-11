"""Definitions for pulsatrix sensors exposed via MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.helpers.entity import EntityDescription

_LOGGER = logging.getLogger(__name__)


class PxChargerStatusCodes:
    states = {
        "IDLE": "Idle",
        "AWAITING_START": "Awaiting Start",
        "AWAITING_AUTHORIZATION": "Awaiting Authorization",
        "STARTING": "Starting",
        "SUSPENDED_EVSE": "Not offering charging",
        "SUSPENDED_EV": "Offered charging but not taking",
        "CHARGING": "Charging",
        "FAILED": "Failed",
        "STOPPED": "Stopped externally",
        "LINGERING": "Wait for EV to reconnect",
        "COMPLETE": "Completed",
        "COMPLETED": "Completed"
    }

    connector_status = {
        "Available": "Available",
        "Occupied": "Occupied",
        "Reserved": "Reserved",
        "Unavailable": "Unavailable",
        "Faulted": "Faulted"
    }

    charge_controller_status = {
        "A1": "Standby",
        "B1": "Vehicle detected",
        "C1": "Charge request",
        "D1": "Charge & vent request",
        "E1": "Shut off",
        "F1": "Error",
        "S1": "Restart after error",
        "R1": "Diode fail",
        "B2": "Charging offered",
        "C2": "Charging",
        "D2": "Charging + venting"
    }

    vehicle_status = {
        "S": "Startup / unknown",
        "A": "Disconnected",
        "B": "Connected",
        "C": "Charge request",
        "D": "Charge & ventilation request",
        "E": "Short circuit",
        "F": "Error",
        "R": "Diode fail"
    }

    start_reason = {
        "Authorized": "Authorized",
        "CablePluggedIn": "Cable plugged in",
        "ChargingRateChanged": "Charging rate changed",
        "ChargingStateChanged": "Charging state changed",
        "Deauthorized": "Deauthorized",
        "EnergyLimitReached": "Energy limit reached",
        "EVCommunicationLost": "EV communication lost",
        "EVConnectTimeout": "EV connect timeout",
        "MeterValueClock": "Meter value clock",
        "MeterValuePeriodic": "Meter value periodic",
        "TimeLimitReached": "Time limit reached",
        "Trigger": "Triggered by CSMS",
        "UnlockCommand": "Unlock command",
        "StopAuthorized": "Stop authorized",
        "EVDeparted": "EV departed",
        "EVDetected": "EV detected",
        "RemoteStop": "Remote stop",
        "RemoteStart": "Remote start",
        "AbnormalCondition": "Abnormal condition",
        "SignedDataReceived": "Signed data received",
        "ResetCommand": "Reset command"
    }

    cp_error_cause = {
        "EvDisconnect": "EV unexpectedly disconnected",
        "EvNotStopping": "EV does not stop when commanded",
        "SignalledAmperageExceeded": "EV exceeds amperage limit",
        "CpShortCircuit": "CP shorted",
        "CpDiodeShortCircuit": "Diode shorted",
        "VentilationNotAvailable": "Ventilation not available"
    }


@dataclass
class PxChargerEntityDescription(EntityDescription):
    """Generic entity description for pulsatrix."""

    state: Callable | None = None
    attribute: str = "0"
    initial_value: bool | str | float | None = None
    attribute_index: int = -1
    domain: str = "generic"
    topic: str = "tx/status"
    raw_value: Callable | None = None
    disabled: bool | None = None
    disabled_reason: str | None = None

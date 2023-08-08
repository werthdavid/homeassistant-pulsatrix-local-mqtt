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
        "COMPLETE": "Completed"
    }



@dataclass
class PxChargerEntityDescription(EntityDescription):
    """Generic entity description for pulsatrix."""

    state: Callable | None = None
    attribute: str = "0"
    attribute_index: int = -1
    domain: str = "generic"
    topic: str = "tx/status"
    disabled: bool | None = None
    disabled_reason: str | None = None
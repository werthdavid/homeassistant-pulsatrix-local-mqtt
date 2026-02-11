"""Definitions for pulsatrix number entities exposed via MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberEntityDescription, NumberMode
from homeassistant.const import UnitOfElectricCurrent, UnitOfPower, UnitOfTime, PERCENTAGE

from . import PxChargerEntityDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class PxChargerNumberEntityDescription(
    PxChargerEntityDescription, NumberEntityDescription
):
    """Number entity description for pulsatrix."""

    domain: str = "number"
    native_value: float | None = None
    native_min_value: float = 0
    native_max_value: float = 100
    native_step: float = 1
    mode: NumberMode = NumberMode.AUTO
    value_formatter: Callable[[float], str] | None = None


def format_float(value: float) -> str:
    """Format float value for MQTT."""
    return str(value)


def format_int(value: float) -> str:
    """Format as integer for MQTT."""
    return str(int(value))


def format_minutes_to_ms(value: float) -> str:
    """Convert minutes to milliseconds for MQTT."""
    return str(int(value * 60000))


NUMBERS: tuple[PxChargerNumberEntityDescription, ...] = (
    PxChargerNumberEntityDescription(
        key="amperage_limit",
        topic="charging/amperageLimit",
        name="pulsatrix Amperage Limit",
        native_value=16,
        native_min_value=6,
        native_max_value=32,
        native_step=0.5,
        mode=NumberMode.SLIDER,
        value_formatter=format_float,
        icon="mdi:current-ac",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerNumberEntityDescription(
        key="power_limit",
        topic="charging/powerLimit",
        name="pulsatrix Power Limit",
        native_value=11000,
        native_min_value=1380,  # ~6A * 230V
        native_max_value=22000,  # ~32A * 230V * 3 phases
        native_step=100,
        mode=NumberMode.BOX,
        value_formatter=format_int,
        icon="mdi:flash",
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_registry_enabled_default=True,
        disabled=False,
    ),
    PxChargerNumberEntityDescription(
        key="limit_timeout",
        topic="charging/limitTimeout",
        name="pulsatrix Limit Timeout",
        native_value=5,  # 5 minutes default
        native_min_value=1,   # 1 minute
        native_max_value=60,  # 1 hour
        native_step=1,  # 1 minute steps
        mode=NumberMode.SLIDER,
        value_formatter=format_minutes_to_ms,
        icon="mdi:timer-outline",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        entity_registry_enabled_default=False,
        disabled=False,
    ),
)

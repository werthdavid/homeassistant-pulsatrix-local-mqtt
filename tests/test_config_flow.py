"""Test the pulsatrix (MQTT) config flow."""
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import RESULT_TYPE_CREATE_ENTRY, RESULT_TYPE_FORM

from custom_components.pulsatrix_local_mqtt.const import DOMAIN


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == RESULT_TYPE_FORM
    assert result["errors"] is None

    with patch(
        "custom_components.pulsatrix_local_mqtt.config_flow.PlaceholderHub.validate_device_topic",
        return_value=True,
    ), patch(
        "custom_components.pulsatrix_local_mqtt.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"serial_number": "0F7E9A442C7B", "topic_prefix": "/pulsatrix"},
        )
        await hass.async_block_till_done()

    assert result2["type"] == RESULT_TYPE_CREATE_ENTRY
    assert result2["title"] == "pulsatrix charger 0F7E9A442C7B"
    assert result2["data"] == {
        "serial_number": "0F7E9A442C7B",
        "topic_prefix": "/pulsatrix",
    }
    assert len(mock_setup_entry.mock_calls) == 1

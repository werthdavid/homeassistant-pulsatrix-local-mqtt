<img width="50%" src="https://app.pulsatrix.net/assets/logo/pulsatrix-07_white.svg"/>

# homeassistant-pulsatrix-local-mqtt

![GitHub actions](https://github.com/werthdavid/homeassistant-pulsatrix-local-mqtt/actions/workflows/pytest.yaml/badge.svg)
![GitHub actions](https://github.com/werthdavid/homeassistant-pulsatrix-local-mqtt/actions/workflows/hassfest.yaml/badge.svg)
![GitHub actions](https://github.com/werthdavid/homeassistant-pulsatrix-local-mqtt/actions/workflows/hacs.yaml/badge.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[!["Buy Me A Coffee"](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/werthdavid)

This is a custom component for Home Assistant to integrate the pulsatrix charger (v3) using the MQTT API (v2).

:exclamation: **This is an unofficial plugin that is not officially supported by pulsatrix**

## Installation

### Prerequisites

- install an MQTT Broker (preferrably Mosquitto). Either via "Addons" (if you use Home Assitant OS) or manually on your OS
- contact [pulsatrix support](mailto:support@pulsatrix.de) and ask them to link the devices to the MQTT Broker
- they will ask you for the IP/Hostname of the MQTT Broker within the current network as it needs to be reachable from the charging controller
- in Home Assistant add the MQTT Integration and configure it to the freshly installed MQTT Broker

### HACS

Use HACS to install this custom component.

### Manual

- Clone the repo
- copy the folder custom_components/pulsatrix_local_mqtt to your custom_components folder
- restart Home Assistant

## Configuration

Use the Web UI (Config flow) to add the "pulsatrix" integration. You have to know the `serial number` (12 digits) of your device. 

![find the serial](serial.png)


## Entities

### Controls (Number Entities)

These entities allow you to control the charging limits of your pulsatrix charger.

| Friendly name      | Type   | Enabled per default  | Range              | Description                                      |
|--------------------|--------|----------------------|--------------------|--------------------------------------------------|
| Amperage Limit     | number | :heavy_check_mark:   | 6-32 A (0.5 steps) | Set the maximum amperage for charging            |
| Power Limit        | number | :heavy_check_mark:   | 1.4-22 kW          | Set the maximum power for charging               |
| Limit Timeout      | number | :white_large_square: | 1-60 min           | How long the limit remains valid before expiring |

> **Note:** The charger always uses the **minimum** of all active limits (API, hardware, cable rating, etc.). Setting a limit below 6A will pause charging. Limits above the `effectiveAmperageLimit` are capped automatically.

### Binary Sensors

| Friendly name        | Category     | Enabled per default  | Description                                           |
|----------------------|--------------|----------------------|-------------------------------------------------------|
| Charging             | `diagnostic` | :heavy_check_mark:   | Whether the EV is charging or not                     |
| Plug Retention Lock  | `diagnostic` | :heavy_check_mark:   | Whether the charging plug is locked                   |
| Connector Available  | `diagnostic` | :heavy_check_mark:   | Whether the connector is available for a new session  |
| Connector Faulted    | `diagnostic` | :heavy_check_mark:   | Whether the connector has reported an error           |
| Vehicle Connected    | `diagnostic` | :heavy_check_mark:   | Whether a vehicle is connected to the charger         |

### Sensors

#### Status Sensors

| Friendly name              | Category     | Enabled per default  | Description                                          |
|----------------------------|--------------|----------------------|------------------------------------------------------|
| State                      | -            | :heavy_check_mark:   | The state of the controller (see below)              |
| Connector Status           | -            | :heavy_check_mark:   | Status of the charging connector                     |
| Charge Controller Status   | `diagnostic` | :heavy_check_mark:   | IEC 61851 status of the SECC                         |
| Vehicle Status             | -            | :heavy_check_mark:   | IEC 61851 status of the connected EV                 |

#### Power & Energy Sensors

| Friendly name              | Category     | Enabled per default  | Description                                          |
|----------------------------|--------------|----------------------|------------------------------------------------------|
| Current Consumption        | `diagnostic` | :heavy_check_mark:   | The current power consumption in kW                  |
| Energy                     | `diagnostic` | :heavy_check_mark:   | The transferred energy of the current session in kWh |
| Total Energy Imported      | `diagnostic` | :heavy_check_mark:   | Total energy imported by the charger in kWh          |
| Max Consumption            | `diagnostic` | :heavy_check_mark:   | Maximum allowed consumption based on limits          |
| Available Amperage         | `diagnostic` | :heavy_check_mark:   | Amperage available before ISO 61851 adjustments      |
| Signaled Amperage          | `diagnostic` | :heavy_check_mark:   | Amperage signaled to the EV                          |
| Charging Duration          | -            | :heavy_check_mark:   | Duration of the current charging session in minutes  |

#### Fiscal Meter Sensors (per phase)

| Friendly name   | Category     | Enabled per default  | Description               |
|-----------------|--------------|----------------------|---------------------------|
| Frequency       | `diagnostic` | :white_large_square: | The grid frequency in Hz  |
| P1/P2/P3 Voltage| `diagnostic` | :white_large_square: | Phase voltage in V        |
| P1/P2/P3 Amperage| `diagnostic`| :white_large_square: | Phase amperage in A       |

#### Grid Meter Sensors

| Friendly name         | Category     | Enabled per default  | Description                                    |
|-----------------------|--------------|----------------------|------------------------------------------------|
| Grid Power            | `diagnostic` | :white_large_square: | Current power at the grid connection point     |
| Grid Energy Imported  | `diagnostic` | :white_large_square: | Total energy imported at the grid connection   |
| Grid Frequency        | `diagnostic` | :white_large_square: | Grid frequency in Hz                           |
| Grid P1/P2/P3 Voltage | `diagnostic` | :white_large_square: | Per phase voltage at grid connection           |
| Grid P1/P2/P3 Amperage| `diagnostic` | :white_large_square: | Per phase amperage at grid connection          |

#### Transaction Sensors

| Friendly name                | Category     | Enabled per default  | Description                                    |
|------------------------------|--------------|----------------------|------------------------------------------------|
| Started Time                 | `diagnostic` | :heavy_check_mark:   | When the charging session started              |
| Ended Time                   | `diagnostic` | :white_large_square: | When the charging session ended                |
| Transaction ID               | `diagnostic` | :white_large_square: | UUID of the current transaction                |
| Start Reason                 | `diagnostic` | :white_large_square: | Reason why charging was started                |
| Energy Active Import Register| `diagnostic` | :white_large_square: | Cumulative active energy imported              |
| Last Active Power            | `diagnostic` | :white_large_square: | Current active power from tx/status            |
| Meter Start                  | `diagnostic` | :white_large_square: | Meter value at session start                   |
| Meter Stop                   | `diagnostic` | :white_large_square: | Meter value at session end                     |
| Peak Active Power            | `diagnostic` | :white_large_square: | Peak power during the session                  |
| Used Phases                  | `diagnostic` | :white_large_square: | Phases used in the current session             |
| Recent CP Error Cause        | `diagnostic` | :white_large_square: | Recent control pilot error cause               |


`diagnostic`: An entity exposing some configuration parameter or diagnostics of a device

### States

The sensor state can have the following states:

| Value                           | Friendly name                                                                                     | Raw Value              |
|---------------------------------|---------------------------------------------------------------------------------------------------|------------------------|
| Idle                            | No transaction in progress                                                                        | IDLE                   |
| Awaiting Start                  | Transaction is currently blocked from starting                                                    | AWAITING_START         |
| Awaiting Authorization          | Transaction is awaiting authorization by some means                                               | AWAITING_AUTHORIZATION |
| Starting                        | Transaction is currently starting (transitional state)                                            | STARTING               |
| Not offering charging           | Vehicle is connected but not offered any charging current                                         | SUSPENDED_EVSE         |
| Offered charging but not taking | Vehicle is connected, offered charging but not taking any                                         | SUSPENDED_EV           |
| Charging                        | Electrical energy is being transferred                                                            | CHARGING               |
| Failed                          | Charging has failed, but the vehicle is still connected                                           | FAILED                 |
| Stopped externally              | The transaction has been stopped by external means                                                | STOPPED                |
| Wait for EV to reconnect        | The transaction is about to end, but lingering to give the user a chance to reconnect the vehicle | LINGERING              |
| Completed                       | The transaction has irrevocably ended and is considered completed                                 | COMPLETED              |

### Connector Status

| Value       | Description                                                       |
|-------------|-------------------------------------------------------------------|
| Available   | Connector is available for a new user                             |
| Occupied    | Connector is occupied and not available                           |
| Reserved    | Connector is reserved via ReserveNow command                      |
| Unavailable | Connector is unavailable due to ChangeAvailability command        |
| Faulted     | Connector has reported an error and is not available              |

### Charge Controller Status (IEC 61851)

| Value | Friendly name        |
|-------|----------------------|
| A1    | Standby              |
| B1    | Vehicle detected     |
| C1    | Charge request       |
| D1    | Charge & vent request|
| E1    | Shut off             |
| F1    | Error                |
| S1    | Restart after error  |
| R1    | Diode fail           |
| B2    | Charging offered     |
| C2    | Charging             |
| D2    | Charging + venting   |

### Vehicle Status (IEC 61851)

| Value | Friendly name              |
|-------|----------------------------|
| S     | Startup / unknown          |
| A     | Disconnected               |
| B     | Connected                  |
| C     | Charge request             |
| D     | Charge & ventilation request|
| E     | Short circuit              |
| F     | Error                      |
| R     | Diode fail                 |

## MQTT Topics

This integration subscribes to and publishes on the following MQTT topics:

### Read Topics (Subscribe)
- `/pulsatrix/secc/<serial>/tx/status` - Transaction status
- `/pulsatrix/secc/<serial>/meter/fiscal` - Fiscal meter data
- `/pulsatrix/secc/<serial>/meter/grid` - Grid meter data
- `/pulsatrix/secc/<serial>/charging/status` - Charging session status
- `/pulsatrix/secc/<serial>/chargingPoint/status` - Charging point status

### Write Topics (Publish)
- `/pulsatrix/secc/<serial>/charging/amperageLimit` - Set amperage limit
- `/pulsatrix/secc/<serial>/charging/powerLimit` - Set power limit
- `/pulsatrix/secc/<serial>/charging/limitTimeout` - Set limit timeout
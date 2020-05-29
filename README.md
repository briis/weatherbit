# // weatherbit
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/briis/weatherbit?include_prereleases&style=flat-square) [![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/custom-components/hacs) [![](https://img.shields.io/badge/COMMUNITY-FORUM-success?style=flat-square)](https://community.home-assistant.io/t/weatherbit-io-current-weather-and-forecast-data/200224)

The weatherbit integration adds support for the *weatherbit.io* web service as a source for meteorological data for your location.

There is currently support for the following device types within Home Assistant:
* Weather
* Sensor

There is only support for *daily* forecasts, as the hourly forecast requires a paid API Key.

## Installation

### HACS Installation
This Integration is part of the default HACS store, so search for *Weatherbit* in HACS.

### Manual Installation

To add Weatherbit to your installation, create this folder structure in your /config directory:

`custom_components/weatherbit`.
Then, drop the following files into that folder:

```yaml
__init__.py
manifest.json
weather.py
sensor.py
entity.py
config_flow.py
const.py
string.json
translation (Directory with all files)
```
## Configuration
The Weatherbit weather service is free under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Generic License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode). Weather data will be pulled once every 30 minutes.

To add Weatherbit weather forecast to your installation, go to the Integrations page inside the configuration panel and add a location by providing the API Key for Weatherbit and longitude/latitude of your location.

If the location is configured in Home Assistant, it will be selected as the default location. After that, you can add additional locations.

During setup you will have the option of installing Individual sensors for each of the *Current Day* values plus the next seven days of Forecast. This will be setup by default, but you can opt not to install them by deselecting the checkbox. If you deselect, and later want the sensors installed, you will have to remove the Integration and then set it up again.

The units used are defined by the Unit System set in the *General* section of the *Configuration* page. If you change the unit system here, you will have to restart Home Assistent for this Integration to reflect the changes.

**You can only add locations through the integrations page, not in configuration files.**

## API Key for Weatherbit
This integration requires an API Key that can be retrieved for free from the Weatherbit Webpage. Please [go here](https://www.weatherbit.io/account/create) to apply for your personal key.
This key allows you to make 500 calls pr. day, and as this Integration uses 4 calls per hour (96 pr day), you can add a maximum of 5 locations to your setup, without exceeding the limit per day.

### CONFIGURATION VARIABLES
**API Key**<br>
&nbsp;&nbsp;*(string)(Required)*<br>
&nbsp;&nbsp;Specify your Weatherbit API Key.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;None

**latitude**<br>
&nbsp;&nbsp;*(float)(Required)*<br>
&nbsp;&nbsp;Manually specify latitude.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;Provided by Home Assistant configuration

**longitude**<br>
&nbsp;&nbsp;*(float)(Required)*.<br>
&nbsp;&nbsp;Manually specify longitude.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;Provided by Home Assistant configuration

**Add Sensors**<br>
&nbsp;&nbsp;*(bool)Optional)*.<br>
&nbsp;&nbsp;Deselect this checkbox of you don't want the sensors added to Home Assistant.

&nbsp;&nbsp;*Default value:*<br>
&nbsp;&nbsp;True

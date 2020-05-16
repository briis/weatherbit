# // weatherbit
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/briis/weatherbit?include_prereleases&style=flat-square) [![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/custom-components/hacs)

The weatherbit integration adds support for the *weatherbit.io* web service as a source for meteorological data for your location.

There is currently support for the following device types within Home Assistant:
* Weather

There is only support for *daily* forecasts, as the hourly forecast requires a paid API Key.

## Installation

### HACS Installation
This Integration is part of the default HACS store, so search for *Weatherbit* in HACS.

### Manual Installation

To add Weatherbit to your installation, create this folder structure in your /config directory:

`custom_components/meteobridge`.
Then, drop the following files into that folder:

```yaml
__init__.py
manifest.json
weather.py
config_flow.py
const.py
string.json
translation (Directory with all files)
```
## Configuration
The Weatherbit weather service is free under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Generic License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode). Weather data will be pulled once every 30 minutes.

To add Weatherbit weather forecast to your installation, go to the Integrations page inside the configuration panel and add a location by providing the API Key for Weatherbit and longitude/latitude of your location.

If the location is configured in Home Assistant, it will be selected as the default location. After that, you can add additional locations.

**You can only add locations through the integrations page, not in configuration files.**

## API Key for Weatherbit
This integration requires an API Key that can be retrieved for free from the Weatherbit Webpage. Please [go here](https://www.weatherbit.io/account/create) to apply for your personal key.
This key allows you to make 500 calls pr. day, and as this Integration uses 4 calls per hour (96 pr day), you can add a maximum of 5 locations to your setup, without exceeding the limit per day.

### CONFIGURATION VARIABLES
**API Key**  
&nbsp;&nbsp;*(string)(Required)*  
&nbsp;&nbsp;Specify your Weatherbit API Key.

&nbsp;&nbsp;*Default value:*  
&nbsp;&nbsp;None

**latitude**  
&nbsp;&nbsp;*(float)(Required)*  
&nbsp;&nbsp;Manually specify latitude.

&nbsp;&nbsp;*Default value:*  
&nbsp;&nbsp;Provided by Home Assistant configuration

**longitude**  
&nbsp;&nbsp;*(float)(Required)*. 
&nbsp;&nbsp;Manually specify longitude.

&nbsp;&nbsp;*Default value:*  
&nbsp;&nbsp;Provided by Home Assistant configuration

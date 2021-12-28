# // weatherbit
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/briis/weatherbit?include_prereleases&style=flat-square) [![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/custom-components/hacs) [![](https://img.shields.io/badge/COMMUNITY-FORUM-success?style=flat-square)](https://community.home-assistant.io/t/weatherbit-io-current-weather-and-forecast-data/200224)

The weatherbit integration adds support for the [weatherbit.io](https://www.weatherbit.io/) web service as a source for meteorological data for your location.

The integration only supports the [Free Tier API](https://www.weatherbit.io/pricing) from Weatherbit and as such is limited in what data we can bring. The *Free Tier* has a maximum of 500 calls per day.

There is currently support for the following device types within Home Assistant:
* Weather
  * One Weather Entity will be created showing Day Based forecast for the next 16 days
* Sensor
  * A whole range of individual sensors will be available. for a complete list of the sensors, see the list below.

## Installation

### HACS Installation
This Integration is part of the default HACS store, so search for *Weatherbit* in HACS.

### Manual Installation

To add Weatherbit to your installation, create this folder structure in your /config directory:

`custom_components/weatherbit`.
Then, drop the following files into that folder:

```yaml
__init__.py
config_flow.py
const.py
entity.py
manifest.json
models.py
sensor.py
weather.py
translation (Directory with all files)
```
## Configuration
The Weatherbit weather service is free under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Generic License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

To add Weatherbit to your installation, do the following:
- Go to *Configuration* and *Integrations*
- Click the `+ ADD INTEGRATION` button in the lower right corner.
- Search for Weatherbit and click the integration.
- When loaded, there will be a configuration box, where you have to enter your *API Key* and *Latitude, Longitude* to get access to your data. When entered click *Submit* and the Integration will load all the entities. Latitude and Longitude are pre-filled with the location you entered in Home Assistant.

If you want to change the update frequencies for the sensor data and forecast data, or select a different language for the Forecast Text, this can be done by clicking `CONFIGURE` in the lower left corner of the Weatherbit integration..

You can configure more than 1 instance of the Integration by using a different Latitude/Longitude. Just remember to adjust the update frequencies due to the limits on the Free Tier.

### API Key for Weatherbit
This integration requires an API Key that can be retrieved for free from the Weatherbit Webpage. Please [go here](https://www.weatherbit.io/account/create) to apply for your personal key.
This key allows you to make 500 calls pr. day. With the default update frequencies this means that you have used 336 calls per day. So if you want to have more than 1 location, you will need to make less frequent updates per location.

### Configuration Variables
* `API Key`: (required) A Personal API Key retrieved from WeatherBit (See above).
* `Latitude`: (required) Latitude of the location needing data from. (Default Latitude from Home Assistant).
* `Longitude`: (required) Longitude of the location needing data from. (Default Longitude from Home Assistant).
* `Update Interval`: (optional) Interval in minutes between sensor updates (Default 5 min).
* `Forecast Interval`: (optional) Interval between in minutes forecast updates (Default 30 min).
* `Forecast Language`: (optional) The language for the forecast text strings returned from Weatherbit. (Default English).

## Available Sensors

Here is the list of sensors that the program generates. Calculated Sensor means, if No, then data comes directly from the Weatherbit, if yes, it is a sensor that is derived from some of the other sensors.

All entities are prefixed with `weatherbit_` and names are prefixed with `Weatherbit`

| Sensor ID   | Name   | Description   | Calculated Sensor   |
| --- | --- | --- | --- |
| air_quality_index | Air Quality Index | Air Quality Index [US - EPA standard 0 - +500]| No |
| air_temperature | Air Temperature | Outside Temperature | No |
| apparent_temperature | Apparent Temperature | The apparent temperature, a mix of Heat Index and Wind Chill | No |
| beaufort | Beaufort Scale | Beaufort scale is an empirical measure that relates wind speed to observed conditions at sea or on land | Yes ||
| beaufort_description | Beaufort Description | A descriptive text for the current Beaufort level. | Yes ||
| cloud_coverage | Cloud Coverage | Cloud coverage (%). | No |
| dew_point | Dew Point | Dewpoint in degrees | No |
| forecast_day_1..7 | Forecast Day 1..7 | Seven sensors holding the Forecast for the next 7 days. Details for the day is in the attributes | No |
| observation_time | Observation Time | Last update time of the data from the station. | No |
| precipitation | Rain Rate | How much is it raining right now | No |
| relative_humidity | Humidity | Relative Humidity | No |
| sealevel_pressure | Sea Level Pressure | Preasure measurement at Sea Level | No |
| snow | Snow Rate | How much is it snowing right now | No |
| solar_radiation | Solar Radiation | Electromagnetic radiation emitted by the sun | No |
| station_pressure | Station Pressure | Pressure measurement where the station is located | No |
| uv_index | UV Index | The UV index | No |
| uv_description | UV Description | A descriptive text for the current UV index | Yes |
| visibility | Visibility | Distance to the horizon | No |
| weather_alerts | Weather Alerts | Number of Alerts for the location. More details are found in the Attributes of that sensor if there are any alerts. | No |
| weather_description | Current Condition | The current condition in the selected Forecast Language | No |
| wind_cardinal | Wind Cardinal | Current measured Wind bearing as text | Yes |
| wind_direction | Wind Direction | Current measured Wind bearing in degrees | No |
| wind_speed | Wind Speed | Current measured Wind Speed in Home Assistant units | No |
| wind_speed_km_h | Wind Speed (km/h) | Current measured Wind Speed in km/h | No |
| wind_speed_knots | Wind Speed (knots) | Current measured Wind Speed in knots | No |

## Available Weather Entities

Here is the list of Weather Entities that the program generates. With the exception of the condition state and the icon, the values for the current condition are equal to the Sensor values, so the Weather entity displayes realtime values and the forecast for either the next days or the next hours. Both entities are installed.

**Note** There has been some recent changes in the units chosen for the Weather Entity, especially for metric users. Pressure units now default to `Pa` so you will see a value of 100.000 for a hPa/Mb value of 1000. Also Wind Speed is now reported as m/s, where it was previously km/h. This is outside the influence of this Integration.

| Sensor ID   | Name   | Description   |
| --- | --- | --- |
| weatherbit | Weatherbit | A weather entity with Forecast for today and the next 15 days |

## Enable Debug Logging

If logs are needed for debugging or reporting an issue, use the following configuration.yaml:

```yaml
logger:
  default: error
  logs:
    custom_components.weatherbit: debug
```

## Contribute to the Project and developing with a Devcontainer

### Integration

1. Fork and clone the repository.
2. Open in VSCode and choose to open in devcontainer. Must have VSCode devcontainer prerequisites.
3. Run the command container start from VSCode terminal
4. A fresh Home Assistant test instance will install and will eventually be running on port 9126 with this integration running
5. When the container is running, go to http://localhost:9126 and the add WeatherFlow Weather from the Integration Page.

### Frontend

There are some sensors in this integration that provides a text as state which is not covered by the core Frontend translation. Example: `sensor.weatherbit_beaufort_description`, `sensor.weatherbit_uv_description` and `sensor.weatherbit_wind_cardinal`.

As default the text in the Frontend is displayed in english if your language is not present in this integration, but if you want to help translate these texts in to a new language, please do the following:
- Go to the `translations` directory under `custom_components/weatherbit` and copy the file `sensor.en.json` to `sensor.YOUR_LANGUAGE_CODE.json` in a directory on your computer.
- Edit the file and change all the descriptions to your language.
- Make a Pull request in this Github and attach your new file.

The same procedure applies for the Configuration flow, follow the above procedure, just copy `en.json` to `YOUR_LANGUAGE_CODE.json`.
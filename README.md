# // weatherbit
The weatherbit integration adds support for the *weatherbit.io* web service as a source for meteorological data for your location.

There is currently support for the following device types within Home Assistant:
* Weather

## Configuration
The Weatherbit weather service is free under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Generic License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode). Weather data will be pulled once every 30 minutes.

To add Weatherbit weather forecast to your installation, go to the Integrations page inside the configuration panel and add a location by providing the API Key for Weatherbit and longitude/latitude of your location.

If the location is configured in Home Assistant, it will be selected as the default location. After that, you can add additional locations.

**You can only add locations through the integrations page, not in configuration files.**

## API Key for Weatherbit
This integration requires an API Key that can be retrieved for free from the Weatherbit Webpage. Please [go here](https://www.weatherbit.io/account/create) to apply for your personal key.
This key allows you to make 500 calls pr. day, and as this Integration uses 4 calls per hour (96 pr day), you can add a maximum of 5 locations to your setup, without exceeding the limit per day.

## CONFIGURATION VARIABLES
**latitude**
*(float)(Required)*

Manually specify latitude.

*Default value:*

Provided by Home Assistant configuration

longitude
(float)(Optional)

Manually specify longitude.

Default value:

Provided by Home Assistant configuration

name
(string)(Optional)

Name to use in the frontend.

Default value:

Home
# Change Log

## [1.0.21] - 2024-01-06

- Fix issue [#94](https://github.com/briis/weatherbit/issues/94) and [#93](https://github.com/briis/weatherbit/issues/93).

**Note** Issue [#91](https://github.com/briis/weatherbit/issues/91) might not get fixed, leaving the Integration unusable as of 2024.3. It is too complicated to maintain this integration due to the low number of calls per day, so testing changes is very difficult as I quickly run out of calls, making me wait until the next day, to be able to continue. I strongly suggest people to find another Weather Integration, and there are many great ones out there.

## [1.0.20] - 2023-05-05

- Fix issue #90 and changed the text in the Config Flow to reflect the new default values for updates

## [1.0.19] - 2023-02-04

- Fixing missing translation string in `pl.json`. Thanks you to @nepozs
- Fix issue [#87](https://github.com/briis/weatherbit/issues/87) Detected integration that called async_setup_platforms. This call has now been replaced by the proper new function.

## [1.0.18] - 2023-01-05

- Fixing *invalid units* for Wind Speed Knots and km/h plus AQI.
- Issue [#85](https://github.com/briis/weatherbit/issues/85)  Removed all deprecated device classes and implemetend `translation_key` to continue translating certain values in the UI.
- Cleaned up the code to use the correct Device Classes based on all the new changes in 2023.1
- Minimum required version from now on is 2023.1.x

## [1.0.17] - 2022-11-07

- Fixing [#84](https://github.com/briis/weatherbit/issues/84) On sensor.weatherbit_forecast_day_n, the native_temperature and native_templow attributes both have the forecasted high temp values if the system is setup for Imperial Units.

## [1.0.16] - 2022-11-03

- Fixing issue [#81](https://github.com/briis/weatherbit/issues/81) and [#82](https://github.com/briis/weatherbit/issues/82). Needs testing.
- Fixing wrong constant definitions for Units

## [1.0.15] - 2022-10-22

### Changed

- Fixing issue [#73](https://github.com/briis/weatherbit/issues/73) **BREAKING CHANGE** This version now completely removes the Alerts from Weatherbit. As it turned out, even though I only did 1 REST call to Weatherbit to get Current, Forecast and Alert Data, the Alert data counted as an extra call. So by removing this, the Integration is a bit more usefull, after Weatherbit reduced the number of Free Calls per day from 500 down to 50.
Removing the Alert part is the best option, as this data is available in a few other specialized integrations like [MeteoAlarm](https://www.home-assistant.io/integrations/meteoalarm/).


## [1.0.14] - 2022-10-13

### Fixed

- Issue [#78](https://github.com/briis/weatherbit/issues/78) Deprecation warning in Logs after 2022.10 upgrade for temperature utility bug
- Issue [[#73](https://github.com/briis/weatherbit/issues/73)] WeatherBit have reduced the available calls per day on the Free Tier from 500 to only 50 calls per day. This now adjusts the minimum and maximum values for the update frequencies to ensure we don't run over the limit. **IF YOU UPGRADE FROM A PREVIOUS VERSION, YOU WILL HAVE TO ADJUST BOTH SENSOR AND FORECAST FREQUENCY MANUALLY**. Set them both to min 60 min to avoid to many calls.

## [1.0.13] - 2022-10-06

### Fixed

- Issue [#76](https://github.com/briis/weatherbit/issues/76) HA 2022.10: Detected integration that uses speed utility

### Changed

- Added Device Class for Wind Speed and Precipitation. This is a new device class introduced with HA 2022.10, that makes it possible to change the unit directly from the UI.


## [1.0.11] - 2022-06-27

### Fixed

- Issue [#70](https://github.com/briis/weatherbit/issues/70) Fixing `is overriding deprecated methods on an instance of WeatherEntity` message that will start showing up in the log. Thanks to @Mariusthvdb for reporting this.


## [1.0.10] - 2022-05-26

### Fixed
- Issue [#67](https://github.com/briis/weatherbit/issues/67). Deprecreated function as of HA V2022.6.


## [1.0.9] - 2022-04-19

### Changed

- Reverting `observation_time` back to a Timestamp device class, but keeping the fix from 1.0.8 with the Timezone.

### Fixed

- Issue [#55](https://github.com/briis/weatherbit/issues/55). Sometimes Weatherbit will deliver the samme alerts message twice. There is now a filter that takes out these double alerts and only displays it once.
- Issue [[#62](https://github.com/briis/weatherbit/issues/62)] and issue [#64](https://github.com/briis/weatherbit/issues/64) Forecast Day is a day behind.

## [1.0.8] - 2022-01-29

### Changed

- German translation for Config Flow and Sensor State update. Thank you @andilge for updating this.

### Fixed

- Issue [#60](https://github.com/briis/weatherbit/issues/60) `observation_time` will now display a Local Date Time string.


## [1.0.7] - 2022-01-21

### Fixed

- Issue [#56](https://github.com/briis/weatherbit/issues/56) Polish language was falling back to English if HA Locale was not set correctly. Thanks to @andilge for spotting and fixing this.
- Issue [#53](https://github.com/briis/weatherbit/issues/53) Ensure humidity sensor is always reported as integer, without decimals.

### Added

- Added French translation of Config Flow. Thank you to @papo-o

## [1.0.6] - 2022-01-05

### Fixed

- **BREAKING CHANGE** [#52](https://github.com/briis/weatherbit/issues/52) Changed Unique ID to use the supplied Latitude and Longitude. The previous value could sometimes change when many stations in close proximity, creating double entries. This unfortunately means that all entities will get a new unique id, and will be duplicated. I recommend to simply delete the Integration and add it again, and all the names should stay the same as before.

- Fixing forecast date not in right format. Date needs to be a UTC time *string* and not DateTime object.


## [1.0.5] - 2021-12-29

### Fixed

- Issue [#50](https://github.com/briis/weatherbit/issues/50) Fixed pressure and visibility values not being correct. **Please note** that when clicking on a weather card, the units for pressure will be reported as `psi` if imperial units or else as `pa`. The values however are in `inHg` and `hPa`. For metric units, wind speed is now also in `m/s` and not `kmh`. Not sure why this was changed on the Weather Entity.


## [1.0.4] - 2021-12-28

### Changed

- Issue [#50](https://github.com/briis/weatherbit/issues/50) Changed the weather entity to use data from the current dataset, so that sensors and the weather entity are in sync on relevant data points.


## [1.0.3] - 2021-12-26

### If you are currently running a version smaller than 1.0.0, then please read the release notes for V1.0.0 before you upgrade

### Added

- New sensor called `observation_time` added. Holds the last update time of the data from the station.


## [1.0.2] - 2021-12-24

### If you are currently running a version smaller than 1.0.0, then please read the release notes for V1.0.0 before you upgrade

### Fixed

- Issue #46. Values for the `forecast_day_X` attributes, were not correct if unit system equals Imperial.

### Changed

- Polish Sensor string updated. Thank you to @nepozs

### Added

- Issue #47. Adding `alt_condition` as attribute to Weather entity. This attribute holds alternative conditions if it is night.


## [1.0.1] - 2021-12-23

### If you are currently running a version smaller than 1.0.0, then please read the release notes for V1.0.0 before you upgrade

### Added

- Issue #43. Added the `forecast_day_X` sensors back as per request. Changed the naming of some of the attributes to be in line with Home Assistant standards.
- Issue #45. City Name is now part of the Attributes for Alerts.

### Changed

- Issue #44. **BREAKING CHANGE** Changed the name of the weather entity to `weather.weatherbit` and the Friendly Name to `Weatherbit` as the previous chosen name was too long. The entity name might stay unchanged, but for some installations it will not, so you might have to update the UI.

### Fixed

- Changed the formula to extract English and Local Language text from the Alerts, to ensure they were in the right order every time.


## [1.0.0] - 2021-12-22

## This release contains breaking changes and you will have to re-define most of your settings in the UI and in automations after installation.

### Upgrade Instructions

Due to the many changes and entities that have been removed and replaced, we recommend the following process to upgrade from an earlier Beta or from an earlier release:

- Upgrade the Integration files, either through HACS (Recommended) or by copying the files manually to your custom_components/weatherbit directory.
- Restart Home Assistant
- Remove the Weatherbit Integration by going to the Integrations page, click the 3 dots in the lower right corner of the Weatherbit Integration and select Delete
- While still on this page, click the + ADD INTEGRATION button in the lower right corner, search for WeatherBit, and start the installation, supplying your credentials.

### Changes

- **BREAKING CHANGE** This is basically a completely new Integration, as all code has been rewritten from the beginning. This goes for the Integration itself, but also for the module `pyweatherbitdata` that this integration uses for communincating with the WeatherBit API. This is done to make the Integration compliant with Home Assistant coding practices and to ensure it is much easier to maintain going forward. As a consequence of that almost all sensors have a new Name and a new Unique ID's, which is why a removal and re-installation is the best option when upgrading to this version. You will also have to change the sensor  and weather entity names in the UI and in Automations that are based on this Integration.
- **Alerts** are now always pulled from Weatherbit, as I found a way to pull that data together with the Current observation data, so it is only 1 call to Weatherbit. If there are no current alerts there will be no Attributes.
- `forecast_day_x` sensors have been removed from the new Integration. Data is already present as attributes in the `weather` entity, but if someone really needs these, please create an issue in Github and I will look at adding them back.
- Fixing Issue #41 and #42. Deprecated `device_state_attributes`.

### Added
- Frontend Translations are now in place for non-standard text based sensors like Beaufort Description, UV Description and Wind Cardinals. This means that the state of the sensor will always be the same, independend of the UI Language, which makes it easier to make automations that go across UI languages. Please see the README file, if you want to translate to your local language.
- Dutch translation for Config Flow added. Thanks to @erik7
- Dutch translation for Sensor UI Values updated. Thanks to @erik7


## [1.0.0-beta.1] - 2021-12-19

This release contains **breaking changes** and you will have to re-define most of your settings in the UI and in automations after installation.

### Upgrade Instructions
Due to the many changes and entities that have been removed and replaced, we recommend the following process to upgrade from an earlier Beta or from an earlier release:

- Upgrade the Integration files, either through HACS (Recommended) or by copying the files manually to your custom_components/weatherbit directory.
- Restart Home Assistant
- Remove the Weatherbit Integration by going to the Integrations page, click the 3 dots in the lower right corner of the Weatherbit Integration and select Delete
- While still on this page, click the + ADD INTEGRATION button in the lower right corner, search for WeatherBit, and start the installation, supplying your credentials.

### Changes
- **BREAKING CHANGE** This is basically a completely new Integration, as all code has been rewritten from the beginning. This goes for the Integration itself, but also for the module `pyweatherbitdata` that this integration uses for communincating with the WeatherBit API. This is done to make the Integration compliant with Home Assistant coding practices and to ensure it is much easier to maintain going forward. As a consequence of that almost all sensors have a new Name and a new Unique ID's, which is why a removal and re-installation is the best option when upgrading to this version. You will also have to change the sensor  and weather entity names in the UI and in Automations that are based on this Integration.
- **Alerts** are now always pulled from Weatherbit, as I found a way to pull that data together with the Current observation data, so it is only 1 call to Weatherbit. If there are no current alerts there will be no Attributes.
- `forecast_day_x` sensors have been removed from the new Integration. Data is already present as attributes in the `weather` entity, but if someone really needs these, please create an issue in Github and I will look at adding them back.
- Fixing Issue #41 and #42. Deprecated `device_state_attributes`.

### Added
- Frontend Translations are now in place for non-standard text based sensors like Beaufort Description, UV Description and Wind Cardinals. This means that the state of the sensor will always be the same, independend of the UI Language, which makes it easier to make automations that go across UI languages. Please see the README file, if you want to translate to your local language.


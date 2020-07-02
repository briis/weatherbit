### Release 0.29
* Fixed error in IO module that occured when weatherbit could not be contacted.
* Added better error handling during Initialization to flag a retry when Weatherbit could not be contacted.
* Bumped weatherbitpypi to 0.24.7

### Release 0.27
* Fixed error in IO module that occured when weatherbit could not be contacted.
* Bumped weatherbitpypi to 0.24.4

### Release 0.25
* Issue #19 - Added the following new Attributes to the Solar Ration Sensor:
  * **dhi**: Diffuse horizontal solar irradiance (W/m^2)
  * **dni**: Direct normal solar irradiance (W/m^2)
  * **ghi**: Global horizontal solar irradiance (W/m^2)
  * **elev_angle**: Solar elevation angle (degrees)
  * **h_angle**: Solar hour angle (degrees).
  * **sunrise**: The time of the next sunrise at location
  * **sunset**: The time of the next sunset at location

  They were added as Attributes here as they are closely linked to Solar Radiation, and I did not want to create more sensors for values that only a few people will use.
* Added Polish translation for Integration and Options setup. If other people would like to contribute to the translation of the Integration Setup page, please [go here](https://github.com/briis/weatherbit/tree/master/custom_components/weatherbit/translations) and take a copy of the `en.json` file, edit the content and save under your language code. Upload the file to the directory and make a PR or send me the file, and I will add it.
* Updated Dutch Language file for Wind Direction
* Updated [README.md](https://github.com/briis/weatherbit/blob/master/README.md) to show how to disable Sensors if you don't need them all.
* Bumped `weatherbitpypi` to V0.24.1

### Release 0.24
* Language support for Wind Direction Text is now done in the IO Module, as Weatherbit did not handle 8Bit Characters very well. ENE which in danish is ØNØ, was translated to ONO. If I did not get this right for all Languages, please [go here](https://github.com/briis/py-weatherbit/tree/master/weatherbitpypi/translations) and add or change the relevant file. Mail it to me or make a PR.
* Each `weatherbit_forecast_day_x` sensor now has an Attribute called `cloudiness` which shows the forecasted Cloud Cover in %.
* Each `weatherbit_forecast_day_x` sensor now has an Attribute called `snow` which shows the forecasted accumulated snowfall for the day in either mm or inches.
* A new sensor called `weatherbit_snow` is now added that shows the current snowfall in mm/hr or inches/hr.
* Bumped weatherbitpypi to 0.23

### Release 0.23
* Updated Dutch Language file for Beaufort Text
* Added Portugise Language file for Beaufort Text

### Release 0.22
* Added two Beaufort Sensors, one with the [Beaufort Scale](https://en.wikipedia.org/wiki/Beaufort_scale) Value `weatherbit_beaufort_value` and one with the textual representation of that value `weatherbit_beaufort_text`. Default the text is in english but if you set the Forecast Language as described in release 0.21, then this text will also be translated. Not all Weatherbit languages are supported yet, but if you are missing a language [go here](https://github.com/briis/py-weatherbit/tree/master/weatherbitpypi/translations) and take on of the files, and make your translation to your language. Either make a PR or send me the file. The same goes if you find errors in any of the translations.

### Release 0.21
* Added support for setting the **Forecast Language**. When retrieving data from Weatherbit, some of the text strings can be translated in to another language. F.ex the `weather_text` string which gives a text with Forecast. This release now makes it possible to get these strings in local Language. See the README.md for a list of Weatherbit supported languages.

If you are upgrading this Integration, after the restart, go to *Integrations* and select *Options* on the Weatherbit Widget to select a new language. If your are installing from Scratch, you will be asked during Configuration.

Please note, this only affects specific sensors and not the Weather Entity, as language for Weather is handled by Home Assistant.

### Release 0.20
* Changed `datetime` attribute on the `forecast_day_x` sensors to use the correct local date. Please note, that Weatherbit only supplies the date part, so time will always be 00:00:00.
* Added new attribute to the Weather Entity called `alt_condition`. This attribute will show the same data as the `state` with the exception of the *partlycloudy* condition, which will separate between a day and night condition called *partlycloudy_day* and *partlycloudy_night* respectively.

### Release 0.16

* Added **Weather Alerts**. If selected during config, there will now be a new sensor added, called `weather_alerts`. The state of the sensor shows the number of alerts for the selected location, and the Attributes hold the details for the alert. See the README.md file for an example on how to use this.<br>
Update frequency for the Weather Alerts follows what you set for the Forecast - Default 30 min.<br>
**NOTE**: You must remove the Integration and Re-Add it before given the option of adding the Weather Alerts sensor.


### Release 0.14

* Added new sensor `weather_icon` holding the icon code for the current condition. Static icons, that works with this icon code, can be downloaded from [this site](https://www.weatherbit.io/api/meta).
* Added Precipitaion Probability (`precip_prop`) as an attribute for each Forecast Day on the sensors and to the Weather Entity.
* Added Weather Description (`weather_text`) as an attribute for each Forecast Day on the sensors.
* Added Weather Icon Code (`weather_icon`) as an attribute for each Forecast Day on the sensors.

### Release 0.13

* Added Weather Description Sensor. There will be a new sensor created, called `sensor.weatherbit_description` that displays a short text string with the current Weather. It can vary a little from the Current Condition as there are more variances in the Weatherbit API than we have in the Conditions in Home Assistant

### Release 0.12

* Weather Entity now reports `datetime` as UTC Date time in RFC 3339 format, which is what the Lovelace Weathercard expects.
* Sensor Entity now reports `datetime` as Location aware Date time in RFC 3339 format.
* Bumped weatherpypi to 0.13

### Release 0.11

* Changed Imperial Wind Unit from mi/h to mph
* Fixed Rain value not displaying correctly when Imperial units
* Changed Forecast for Weather and Sensor to start with Current Day.

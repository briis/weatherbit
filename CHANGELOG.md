### Release 0.16

* Added **Weather Alerts**. If selected during config, there will now be a new sensor added, called `weather_alerts`. The state of the sensor shows the number of alerts for the selected location, and the Attributes hold the details for the alert. See the README.md file for an example on how to use this.<br>
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

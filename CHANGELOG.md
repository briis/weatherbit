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

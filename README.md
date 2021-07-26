# WeatherAPI

This is an api developed with Django and Django rest framework to get the weather data of a city

### Installation
1- Clone this repository

2- Inside the root folder of the project install the python dependencies
```sh
$ pip install -r requirements.txt
   ```
3- (Optional) Create environment variable for django secret key
```sh
$ export DJANGO_SECRET_KEY=YOUR_SECRET_KEY
   ```
4- enter the WeatherAPI directory and run the Django server
```sh
$ python manage.py runserver
   ```
  
## Usage

 To use the api, send an http request of type get, to the following endpoint: http://localhost:8000/weather adding to the url the parameters of city and country from which you want to get the weather data.
 
 The city is specified with the param name "**city**" and the country with the param name "**country**".
 The country param this must be the code of the country, both parameters are required and the country code must be lowercase.
 
 example:
 
 ```sh
$ curl "http://localhost:8000/weather?city=medellin&country=co"

   ```
  response example:
 ```json
  {"location_name":"Medellín, CO","temperature_c":"17.96 °C","temperature_f":"64.33 °F","wind":"1.03 m/s","cloudiness":"scattered clouds","pressure":"1028 hpa","humidity":"98%","sunrise":"10:56","sunset":"23:21","geo_coordinates":"[-75.5636, 6.2518]","requested_time":"26/07/2021 04:44:57","forecast":{"temp_min_c":"17.81 °C","temp_max_c":"18.87 °C"}}
 ```
 ### Tests

To run the unit tests, go to the WeatherAPI directory and run the following command
```sh
python manage.py test

   ```

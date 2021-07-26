from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from .api_functions import (request_weather_data, kelvin_2_celsius,
                            kelvin_2_fahrenheit, timestamp_2_time,
                            process_data, get_weather_data)


class TestApi(APITestCase):

    @classmethod
    def setUpTestData(cls):
        print("\n" + "#" * 20)
        print("Testing Api")
        print("#" * 20)

    def test_request_api(self):

        print("\ntest_request_api")
        url = '/weather?country=co&city=medellin'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        res_data = response.data
        self.assertTrue('location_name' in res_data)
        self.assertTrue('temperature_c' in res_data)
        self.assertTrue('temperature_f' in res_data)
        self.assertTrue('wind' in res_data)
        self.assertTrue('cloudiness' in res_data)
        self.assertTrue('pressure' in res_data)
        self.assertTrue('humidity' in res_data)
        self.assertTrue('sunrise' in res_data)
        self.assertTrue('sunset' in res_data)
        self.assertTrue('geo_coordinates' in res_data)
        self.assertTrue('requested_time' in res_data)
        self.assertTrue('forecast' in res_data)

    def test_errors_api(self):
        print("test_errors_api")

        # capital letter country
        url = '/weather?country=CO&city=medellin'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        res_message = 'the country parameter cannot have uppercase letters'
        self.assertEqual(response.data["error"], res_message)

        # no city
        url = '/weather?country=co'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        res_message = 'the city parameter is required'
        self.assertEqual(response.data["error"], res_message)

        # no country
        url = '/weather?city=medellin'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        res_message = 'the country parameter is required'
        self.assertEqual(response.data["error"], res_message)

        # numeric country
        url = '/weather?country=12&city=medellin'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        res_message = 'the country must be alphabetic'
        self.assertEqual(response.data["error"], res_message)

        # numeric city
        url = '/weather?country=co&city=434'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        res_message = 'the city must be alphabetic'
        self.assertEqual(response.data["error"], res_message)


class TestFunctions(APITestCase):

    @classmethod
    def setUpTestData(cls):
        print("\n" + "#" * 20)
        print("TestFunctions")
        print("#" * 20)

    def test_request_weather_data_f(self):
        print("test_request_weather_data_f")
        status, data = request_weather_data("bogota", "co")
        self.assertEqual(status, 200)
        self.assertEqual(type(data), type({}))

    def test_kelvin_2_celsius_f(self):
        print("test_kelvin_2_celsius_f")
        cel = kelvin_2_celsius(120)
        self.assertEqual(cel, -153.15)

    def test_kelvin_2_fahrenheit_f(self):
        print("test_kelvin_2_celsius_f")
        far = kelvin_2_fahrenheit(500)
        self.assertEqual(far, 440.33)

    def test_timestamp_2_time_f(self):
        print("test_timestamp_2_time_f")
        timestamp = 1627269534
        time = timestamp_2_time(timestamp)
        self.assertEqual(time, "03:18")

    def test_process_data_f(self):
        print("test_process_data_f")
        input_data = {'coord': {'lon': -75.5636, 'lat': 6.2518},
                      'weather': [{'id': 803, 'main': 'Clouds',
                                   'description': 'broken clouds', 'icon': '04n'}],
                      'base': 'stations', 'main': {'temp': 291.61, 'feels_like': 292.1,
                                                   'temp_min': 290.96, 'temp_max': 292.02, 'pressure': 1027,
                                                   'humidity': 99}, 'visibility': 10000,
                      'wind': {'speed': 1.03, 'deg': 0},
                      'clouds': {'all': 75}, 'dt': 1627269927,
                      'sys': {'type': 2, 'id': 2002201,
                              'country': 'CO', 'sunrise': 1627210569, 'sunset': 1627255266},
                      'timezone': -18000, 'id': 3674962, 'name': 'Medellín', 'cod': 200}
        output_data = process_data(input_data)

        self.assertEqual(output_data["location_name"], "Medellín, CO")
        self.assertEqual(output_data["temperature_c"], "18.46 °C")
        self.assertEqual(output_data["wind"], "1.03 m/s")
        self.assertEqual(output_data["temperature_f"], "65.23 °F")
        self.assertEqual(output_data["cloudiness"], "broken clouds")
        self.assertEqual(output_data["humidity"], "99%")
        self.assertEqual(output_data["sunrise"], "10:56")

    def test_get_weather_data_f(self):

        print("test_get_weather_data_f")
        status, res_data = get_weather_data("medellin", "co")
        self.assertEqual(status, 200)
        self.assertTrue('location_name' in res_data)
        self.assertTrue('temperature_c' in res_data)
        self.assertTrue('temperature_f' in res_data)
        self.assertTrue('wind' in res_data)
        self.assertTrue('cloudiness' in res_data)
        self.assertTrue('pressure' in res_data)
        self.assertTrue('humidity' in res_data)
        self.assertTrue('sunrise' in res_data)
        self.assertTrue('sunset' in res_data)
        self.assertTrue('geo_coordinates' in res_data)
        self.assertTrue('requested_time' in res_data)
        self.assertTrue('forecast' in res_data)

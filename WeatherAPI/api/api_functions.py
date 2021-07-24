from datetime import datetime
import requests


def request_weather_data(city, country):

    base_api_url = 'http://api.openweathermap.org'
    api_url = f'/data/2.5/weather?q={city},{country}' +\
        '&appid=1508a9a4840a5574c822d70ca2132032'
    response = requests.get(base_api_url + api_url)

    return response.status_code, response.json()


def kelvin_2_celsius(kelvin):
    celsius = kelvin - 273.15
    return float("{:.2f}".format(celsius))


def kelvin_2_fahrenheit(kelvin):
    fahren = (1.8 * kelvin) - 459.67
    return float("{:.2f}".format(fahren))


def timestamp_2_time(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%H:%M")


def process_data(data):

    res_data = {}

    res_data["location_name"] = f"{data['name']}, {data['sys']['country']}"

    cel_temp = kelvin_2_celsius(data['main']["temp"])
    res_data["temperature_c"] = f"{str(cel_temp)} °C"

    fahr_temp = kelvin_2_fahrenheit(data['main']["temp"])
    res_data["temperature_f"] = f"{str(fahr_temp)} °F"

    wind = f"{data['wind']['speed']} m/s"
    res_data["wind"] = wind

    cloudiness = data['weather']
    res_data["cloudiness"] = cloudiness[0]['description']

    pressure = data['main']["pressure"]
    res_data["pressure"] = f"{pressure} hpa"

    humidity = data['main']["humidity"]
    res_data["humidity"] = f"{humidity}%"

    sunrise = data['sys']["sunrise"]
    sunrise_time = timestamp_2_time(sunrise)
    res_data["sunrise"] = sunrise_time

    sunset = data['sys']["sunset"]
    sunset_time = timestamp_2_time(sunset)
    res_data["sunset"] = sunset_time

    lon, lat = data['coord']["lon"], data['coord']["lat"]
    res_data["geo_coordinates"] = f"[{str(lon)}, {str(lat)}]"

    res_data["requested_time"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    temp_min_c = kelvin_2_celsius(data["main"]["temp_min"])
    temp_max_c = kelvin_2_celsius(data["main"]["temp_max"])
    forecast = {"temp_min_c": f"{temp_min_c} °C",
                "temp_max_c": f"{temp_max_c} °C"}
    res_data["forecast"] = forecast

    return res_data


def get_weather_data(city, country):

    status, data = request_weather_data(city, country)

    if status != 200:
        print(data)
        return status, data

    res_data = process_data(data)

    return status, res_data

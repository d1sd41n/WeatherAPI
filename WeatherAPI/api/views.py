from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.cache import cache

from .api_functions import get_weather_data


class WeatherView(APIView):
    def get(self, request):

        city = request.query_params.get('city')
        country = request.query_params.get('country')

        if not city:
            return Response({"error": "the city parameter is required"}, status=404)
        elif not country:
            return Response({"error": "the country parameter is required"}, status=404)
        elif len(country) != 2:
            return Response({"error": "the city parameter can only have two characters"},
                            status=404)
        elif any(x.isupper() for x in country):
            return Response({"error": "the country parameter cannot have uppercase letters"},
                            status=404)
        elif city.isnumeric():
            return Response({"error": "the city must be alphabetic"}, status=400)
        elif country.isnumeric():
            return Response({"error": "the country must be alphabetic"}, status=400)

        headers = {"content-type": "application/json"}

        city = city.lower()
        cache_key = city + country
        cache_data = cache.get(cache_key)

        if cache_data:
            return Response(cache_data, headers=headers)

        status, data = get_weather_data(city, country)

        if status != 200:
            return Response({"error": data["message"]}, status=status, headers=headers)

        cache.set(cache_key, data, 120)
        return Response(data, headers=headers)

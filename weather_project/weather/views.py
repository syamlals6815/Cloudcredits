import requests
from django.shortcuts import render

API_KEY = "76cc8e010ea515076047c78e0fd5867c"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def weather_view(request):
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.POST.get("city").strip()

        if city:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if response.status_code == 200:
                weather_data = {
                    "city": data["name"],
                    "temperature": f"{data['main']['temp']}°C",
                    "humidity": f"{data['main']['humidity']}%",
                    "condition": data["weather"][0]["description"].title()
                }
            else:
                error_message = "City not found. Check the spelling and try again."

    return render(request, "weather.html", {"weather": weather_data, "error": error_message})

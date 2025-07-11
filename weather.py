import requests

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key

    def is_bad_weather(self, location, date_time):
        # OpenWeatherMap current weather API
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric"
            response = requests.get(url).json()
            weather = response['weather'][0]['main'].lower()
            return 'rain' in weather or 'storm' in weather or 'snow' in weather
        except:
            return False

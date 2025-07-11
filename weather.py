class WeatherService:
    def is_bad_weather(self, location, date_time):
        # Placeholder for OpenWeatherMap API call
        # For now, fake bad weather on Sundays
        if date_time.weekday() == 6:
            return True
        return False

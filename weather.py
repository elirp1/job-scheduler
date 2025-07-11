class WeatherService:
    def is_bad_weather(self, location, date_time):
        # Placeholder: Sundays = bad weather
        return date_time.weekday() == 6

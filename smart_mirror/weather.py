import requests

def get_weather_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch weather data.")
        return None

def display_weather_details(weather_data, location_name):
    if weather_data:
        print(f"Weather in {location_name}:")
        print("Description:", weather_data['weather'][0]['description'])
        print("Temperature:", weather_data['main']['temp'], "°C")
        print("Humidity:", weather_data['main']['humidity'], "%")
        print("Pressure:", weather_data['main']['pressure'], "hPa")
        print("Wind Speed:", weather_data['wind']['speed'], "m/s")
    else:
        print("No weather data available.")

def get_location_name(latitude, longitude, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=1&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        location_data = response.json()
        if location_data:
            return location_data[0]['name']
        else:
            print("Location data not found.")
            return None
    else:
        print("Failed to fetch location data.")
        return None

def main():
    latitude = 13.0836
    longitude = 80.275
    api_key = 'c9a572a88fa13f639d8819851d9ca37f'

    location_name = get_location_name(latitude, longitude, api_key)
    if location_name:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        weather_data = get_weather_data(url)
        display_weather_details(weather_data, location_name)

if __name__ == "__main__":
    main()

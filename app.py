import requests
from flask import Flask, render_template, request, jsonify
import datetime as dt

app = Flask(__name__)


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = (celsius * 9 / 5) + 32
    return celsius, fahrenheit


def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "units": "metric", "appid": api_key}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            temp_kelvin = data['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(
                temp_kelvin)
            feels_like_kelvin = data['main']['feels_like']
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(
                feels_like_kelvin)
            wind_speed = data['wind']['speed']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            sunrise_time = dt.datetime.utcfromtimestamp(
                data['sys']['sunrise'] + data['timezone'])
            sunset_time = dt.datetime.utcfromtimestamp(
                data['sys']['sunset'] + data['timezone'])
            # print(f"Weather: {weather_description}")
            # print(f"Temperature: {temperature}°C")
            # print(f"Temperature in {city}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
            # print(f"Temperature in {city} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F")
            # print(f"Humidity in {city}: {humidity}%")
            # print(f"Wind Speed in {city}: {wind_speed}m/s")
            # print(f"General Weather in {city}: {description}")
            # print(f"Sun rises in {city} at {sunrise_time} local time.")
            # print(f"Sun sets in {city} at {sunset_time} local time.")
        else:
            error_message = "City not found. Please try again."
            # print("city not found. Please try again.")
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching weather data: {e}")
         # Handle network-related errors
        return {
            "error": "Error fetching weather data: Network error."
        }
    except KeyError:
        # print("Invalid API data. Please try again.")
         # Handle invalid API response
        return {
            "error": "Invalid API data. Please try again."
        }
    except Exception as e:
        # print(f"Something went wrong: {e}")
        # Handle other unexpected errors
        return {
            "error": f"Something went wrong: {e}"
        }
    
    # Return all the data in a dictionary
    return {
                "description": weather_description,
                "temp_celsius": temp_celsius,
                "temp_fahrenheit": temp_fahrenheit,
                "feels_like_celsius": feels_like_celsius,
                "feels_like_fahrenheit": feels_like_fahrenheit,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "city": city,
                "error": None  # No error occurred, so set to None
            }
# def main():
    # api_key = "5f974f5fe2e70a2764bc875d31e2c3ad"
    # city = input("Enter the city name: ")

    # if not city:
    #     print("city name cannot be empty.")
    # else:
    #     get_weather(api_key, city)


# if __name__ == "__main__":
#     main()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = "5f974f5fe2e70a2764bc875d31e2c3ad"
        city = request.form["city"]
        weather_data = get_weather(api_key, city)

        if weather_data["error"]:
            return render_template("error.html", error_message=weather_data["error"])
        else:
            return render_template("weather.html", weather_data=weather_data, city=city)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

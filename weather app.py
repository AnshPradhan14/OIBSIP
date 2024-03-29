import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

def convert_temperature(temp, unit):
    if unit == "Celsius":
        return temp
    elif unit == "Fahrenheit":
        return (temp * 9/5) + 32
    else:
        return temp

def get_weather(api_key, location, unit):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        # Convert temperature if necessary
        if unit != "Celsius":
            data["main"]["temp"] = convert_temperature(data["main"]["temp"], unit)
        return data
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {e}")
        return None

def get_wind_direction(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round((degrees % 360) / 45)
    return directions[index % 8]

def display_weather(data, unit):
    if data is None:
        return "Failed to fetch weather data. Please try again later."

    if "name" not in data:
        return "City not found. Please check the spelling and try again."
    else:
        city = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "Unknown")
        temp = data.get("main", {}).get("temp", "Unknown")
        humidity = data.get("main", {}).get("humidity", "Unknown")
        description = data.get("weather", [{}])[0].get("description", "Unknown")
        icon_id = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", "Unknown")
        wind_direction_deg = data.get("wind", {}).get("deg", "Unknown")
        wind_direction_name = get_wind_direction(wind_direction_deg)

        # Load weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}.png"
        icon_response = requests.get(icon_url)
        icon_data = Image.open(io.BytesIO(icon_response.content))
        weather_icon = ImageTk.PhotoImage(icon_data)

        # Convert temperature if necessary
        if unit != "Celsius":
            temp = convert_temperature(temp, unit)

        # Update weather display
        weather_display.config(
            text=(
                f"Weather for {city}, {country}:\n"
                f"Temperature: {temp}°{unit}\n"
                f"Humidity: {humidity}%\n"
                f"Conditions: {description.capitalize()}\n"
                f"Wind Speed: {wind_speed} m/s\n"
                f"Wind Direction: {wind_direction_name} ({wind_direction_deg}°)"
            ),
            image=weather_icon,
            compound=tk.LEFT
        )
        weather_display.image = weather_icon

def get_weather_data():
    location = location_entry.get()
    unit = unit_var.get()
    weather_data = get_weather(api_key, location, unit)
    display_weather(weather_data, unit)

api_key = "f3c3dbea52b0cf3c4d11ec769ed81419"

# Create GUI window
window = tk.Tk()
window.title("Weather App")

# Create input field
location_label = tk.Label(window, text="Enter a city or ZIP code:")
location_label.pack()
location_entry = tk.Entry(window)
location_entry.pack()

# Create temperature unit selection
unit_var = tk.StringVar()
unit_var.set("Celsius")  # Default unit
unit_label = tk.Label(window, text="Select Temperature Unit:")
unit_label.pack()
celsius_radio = tk.Radiobutton(window, text="Celsius", variable=unit_var, value="Celsius")
celsius_radio.pack()
fahrenheit_radio = tk.Radiobutton(window, text="Fahrenheit", variable=unit_var, value="Fahrenheit")
fahrenheit_radio.pack()

# Create button to fetch weather data
get_weather_button = tk.Button(window, text="Get Weather", command=get_weather_data)
get_weather_button.pack()

# Create weather display label
weather_display = tk.Label(window, text="", wraplength=400)
weather_display.pack()

window.mainloop()

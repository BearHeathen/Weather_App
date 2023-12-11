from tkinter import *
import customtkinter
import requests
from datetime import datetime
from dotenv import load_dotenv
import os



import tkintermapview

# Initialize Window
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("400x600")  # size of the window by default
root.resizable(0, 0)  # to make the window size fixed
# title of our window
root.title("Weather App - bearheathen v0.0.1")

# ----------------------Functions to fetch and display weather info
city_value = StringVar()


def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()


def showWeather():
    # Enter you api key, copies from the OpenWeatherMap dashboard
    load_dotenv()
    api_key = os.environ.get("API_KEY")  # sample API...using dotenv to obfuscate my own API
    print(api_key)

    # Get city name from user from the input field (later in the code)
    city_name = city_value.get()

    # API url
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=' + str(api_key) + '&units=imperial'

    # Get the response from fetched url
    response = requests.get(weather_url)

    # changing response from json to python readable
    weather_info = response.json()
    print(weather_info)

    tfield.delete("1.0", "end")  # to clear the text field for every new output

    # as per API documentation, if the cod is 200, it means that weather data was successfully fetched

    if weather_info['cod'] == 200:

        # -----------Storing the fetched values of weather of a city
        city_name = weather_info['name']
        lat = float(weather_info['coord']['lon'])
        lon = float(weather_info['coord']['lat'])
        temp = int(weather_info['main']['temp'])# - kelvin)  # converting default kelvin value to Celcius
        feels_like_temp = int(weather_info['main']['feels_like'])# - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed']
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        #description = weather_info['alerts']['description']

        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)

        # assigning Values to our weather varaible, to display as output

        weather = f"\nWeather of: {city_name}\nTemperature (Fahrenheit): {temp}°\nFeels like in (Fahrenheit): {feels_like_temp}°\nPressure: {pressure} mm HG\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\n"#Info: {description}
        tfield.insert(INSERT, weather)  # to insert or send value in our Text Field to display output
        createMap(lat, lon)
    else:
        weather = f"\n\tWeather for '{city_name}' not found!\n\tKindly Enter valid City Name !!"
        lat = 0
        lon = 0
        return lat, lon





# ------------------------------Frontend part of code - Interface


city_head = customtkinter.CTkLabel(root, text='Enter City', font=customtkinter.CTkFont('Arial', 14, 'bold'), padx=20, pady=10).pack(pady=10)  # to generate label heading

inp_city = customtkinter.CTkEntry(root, textvariable=city_value, width=240, font=('Arial', 14, 'bold')).pack(padx=20)
customtkinter.CTkButton(master=root, command=showWeather, text="Check Weather").pack(pady=20)

# to show output

weather_now = customtkinter.CTkLabel(root, text="The Weather is:", font=customtkinter.CTkFont('Arial', 12, 'bold')).pack(pady=10)

tfield = Text(root, width=40, height=10)
tfield.pack()

lat, lon = showWeather()
print(lat)
print(lon)
# create map widget
def createMap(lat, lon):
    latitude = lat
    longitude = lon
    print(latitude)
    print(longitude)
    map_widget = tkintermapview.TkinterMapView(root, width=400, height=225, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.80, anchor=customtkinter.CENTER)
    map_widget.set_position(longitude, latitude, marker=True)



root.mainloop()
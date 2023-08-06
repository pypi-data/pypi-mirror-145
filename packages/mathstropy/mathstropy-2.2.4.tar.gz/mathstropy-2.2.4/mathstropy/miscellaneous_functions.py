import random
from .words import words
import json

data = words

def randomword():
    random_word = random.choice(data)
    return random_word

# make word mask function - Mathstronauts library
def wordmask(word):
    #TODO: allow user to specify number of mask letters
    a = random.randint(0, len(word)-1)
    b = random.randint(0, len(word)-1)
    while(a==b):
        b = random.randint(0, len(word)-1)
    wordmask = ""
    for i in range(len(word)):
        if i == a or i == b:
            wordmask += "_"
        else:
            wordmask += word[i]
    return wordmask


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

from datetime import *

# convert all dictionary items to string
def dict_str(dictionary):
    keys_values = dictionary.items()
    new_dict = {
        str(key): str(value) for key, value in keys_values
    }
    return new_dict

# convert from epoch to standard time
def convert_time(time):
    standard_time = datetime.fromtimestamp(time)
    return standard_time

def time_format(time_var):
    int_type = isinstance(time_var, int)
    if int_type == True:  # if the variable is in epoch time, it will be read as an integer and needs to be converted
        time_standard = datetime.fromtimestamp(time_var)
    else:  # else the variable is already in standard time
        time_standard = time_var

    hour = time_standard.strftime('%I')
    minute = time_standard.strftime('%M')
    period = time_standard.strftime('%p')

    combine_time = f"{hour}:{minute} {period}"
    return combine_time

def date_format(date_var):
    int_type = isinstance(date_var, int)
    if int_type == True:  # if the variable is in epoch time, it will be read as an integer and needs to be converted
        date_standard = datetime.fromtimestamp(date_var)
    else:  # else the variable is already in standard time
        date_standard = date_var

    date = date_standard.strftime('%x')
    return date

# Get Coordinate Data from Geocoding API
import requests

geo_URL = "http://api.openweathermap.org/geo/1.0/direct?"
API_KEY = "bc93af7ec21317a25fa7d755f7391e39"

def getLocation(city):
    city_name = city

    geo_parameters = {
        "q": city_name,
        "appid": API_KEY,
    }

    geo_response = requests.get(geo_URL, params=geo_parameters)
    geo_data = geo_response.json()
    geo_first = geo_data[0]  # get first city, multiple cities may be returned in a list
    lat = geo_first["lat"]
    lon = geo_first["lon"]
    return (lat, lon)

# Weather API Parser
def dataformat(data):
    response = data.json()
    keys_to_parse = ["weather", "main", "wind", "dt", "soles"]
    weather_data = {}
    for key in response:
        if key in keys_to_parse:
            if isinstance(response[key], dict):
                for subkey in response[key]:
                    if key == "wind":
                        key_name = key + "_" + subkey
                    else:
                        key_name = subkey
                    weather_data[key_name] = response[key][subkey]
            elif isinstance(response[key], list):
                for subkey in response[key][0]:
                    key_name = subkey
                    weather_data[key_name] = response[key][0][subkey]
            else:
                weather_data[key] = response[key]
    return weather_data


import requests as req
import json

from requests import status_codes

API_KEY = "09e55b3c6482eb81e2895a05b3a8e338"

def get_weather(city="Seoul"):
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}&lang=kr'
    # print(URL)
    weather={}
    res = req.get(URL)
    if res.status_code == 200:
        result = res.json()
        weather['main'] = result['weather'][0]['main']
        weather['description'] = result['weather'][0]['description']
        # print(result['weather'][0]['description'])
        icon = result['weather'][0]['icon']
        weather['icon'] = f'http://openweathermap.org/img/w/{icon}.png'
        weather['etc'] = result['main']
    else:
        print('errer',res,status_codes)

    return weather
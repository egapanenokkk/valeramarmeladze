import requests as r
import geopy
import os
from datetime import datetime


def git_search(query, language='python'):
    url = 'https://api.github.com/search/repositories'
    params = {
        'q': query,
        'l': language
    }
    res = r.get(url, params=params).json()
    message = ''
    for repo in res['items'][:5]:
        message += f'<a href="{repo["svn_url"]}">{repo["name"]}</a>\n'
    return message


def send_image():
    content = r.get('https://random.dog/woof.json').json()
    img_url = content['url']
    return img_url


def get_city(lat, lon):
    locator = geopy.geocoders.Nominatim(user_agent='geoapiExercises')
    location = locator.reverse(str(lat) + ',' + str(lon))
    address = location.raw['address']
    return address


def get_forecast(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat':lat,
        'lon':lon,
        'appid':os.environ.get('WEATHER_APP'),
        'units':'metric',
        'lang':'ru',
    }
    resp = r.get(url, params=params).json()
    return resp
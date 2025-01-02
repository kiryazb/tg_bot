from pprint import pprint

import requests

# Ваш код здесь.
responce = requests.get('https://swapi.py4e.com/api/people/')
characters = responce.json().get('results')[0:10]
pprint(characters)
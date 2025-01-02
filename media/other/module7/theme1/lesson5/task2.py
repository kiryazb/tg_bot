from pprint import pprint

import requests

# Ваш код здесь.
responce = requests.get('https://swapi.py4e.com/api/people/1/')
characters = responce.json()
pprint(characters)

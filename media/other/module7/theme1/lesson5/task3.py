import requests


response = requests.get('https://swapi.py4e.com/api/planets/1/')
diameter = response.json().get('diameter')

print(diameter)
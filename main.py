import requests

r = requests.get('https://pokebuildapi.fr/api/v1/pokemon')
data = r.json()
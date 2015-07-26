import requests
import json

BASE_URL = 'http://pokeapi.co'

def query_pokeapi(resource_url):
    url = '{0}{1}'.format(BASE_URL, resource_url)
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    return None

charizard = query_pokeapi('/api/v1/pokemon/charizard/')

sprite_uri = charizard['sprites'][0]['resource_uri']
description_uri = charizard['descriptions'][0]['resource_uri']

sprite = query_pokeapi(sprite_uri)
description = query_pokeapi(description_uri)

print charizard['name']
print description['description']
print BASE_URL + sprite['image']

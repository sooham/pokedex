import json

import requests

from django.http import HttpResponse
from django_twilio.decorators import twilio_view
from twilio import twiml


@twilio_view
def respondToTwilioRequest(request):
    """ (HttpRequest) -> HttpResponse
        Takes in POST request from Twilio servers and
        returns either help response or pokedex entry.
    """
    if request.method == "GET":
        return HttpResponse("We do not accept GET requests here.")

    message_body = request.POST["Body"]
    pokemon_name = message_body.strip().lower()
    # check if pokemon is in pokedex
    pokedex_entry = check_pokedex(pokemon_name)
    response = twiml.Response()
    if pokedex_entry:
        response.message(
            pokedex_entry['description']
        ).media(pokedex_entry['sprite'])
    else:
        response.message(
            "Pokemon not found. Please type the name of pokemon to search."
        )
    return response


def check_pokedex(pokemon):
    """ (str) -> dict
        Returns a dictionary filled with pokedex data about pokemon
        from pokeAPI. If pokemon does not exist return empty dict.
    """
    json_data = query_pokeapi('/api/v1/pokemon/{0}/'.format(pokemon))
    pokedex_entry = {}
    if json_data:
        sprite_uri = json_data['sprites'][0]['resource_uri']
        description_uri = json_data['descriptions'][0]['resource_uri']
        sprite = query_pokeapi(sprite_uri)
        description = query_pokeapi(description_uri)
        pokedex_entry['description'] = description['description']
        pokedex_entry['sprite'] = "http://pokeapi.co" + sprite['image']
    return pokedex_entry


def query_pokeapi(resource_url):
    """ (str) -> dict
        Returns JSON if resource exists in pokeAPI, else return None.
    """
    BASE_URL = 'http://pokeapi.co'
    url = '{0}{1}'.format(BASE_URL, resource_url)
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    return None

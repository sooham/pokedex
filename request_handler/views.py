import os
import re
import requests
import twilio
import twilio.twiml

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import TwilioRestClient

PKMNS = requests.get("http://pokeapi.co/api/v1/pokedex/1/").json()["pokemon"]
PKMN_NAMES = sorted([pokemon['name'] for pokemon in PKMNS])

client = None


def init_twilio_rest_client():
    """ (NoneType) -> NoneType
    Initiates and stores a fully authenticated twilio.rest.TwilioRestClient
    in variable client. Modifies client global variable
    """
    global client
    try:
        os.environ['TWILIO_ACCOUNT_SID']
        os.environ['TWILIO_AUTH_TOKEN']
    except KeyError:
        return HttpResponseServerError(
            'Twilio credientails not installed on serverside'
        )
    client = TwilioRestClient()


def number(string):
    ''' (str) -> str
    Checks if string contains an numbers only using regex and returns
    the corresponding number. Otherwise returns None.
    '''
    match_obj = re.match("^\s*(\d+)\s*$", string)
    if match_obj:
        return match_obj.group(1)
    else:
        return None


def send_sms(msg):
    ''' (str) -> HttpResponse
    Return the TwiML message verb with msg as a HttpResponse.
    '''
    response = twilio.twiml.Response()
    response.message(msg)
    return HttpResponse(response.toxml(), content_type='text/xml')


def redirect_to(url):
    ''' (str) -> HttpResponse
    Return the TwiML redirect verb with url redirection as HttpResponse.
    '''
    response = twilio.twiml.Response()
    response.redirect(url, method="GET")
    return HttpResponse(response.toxml(), content_type='text/xml')


@csrf_exempt
def sms_input_handler(request):
    ''' Analyses the HTTP POST request from Twilio servers and redirects to
    pokemon by name or number through Twilio requests to the correct views
    '''
    global client
    if not client:
        init_twilio_rest_client()

    if request.method == 'GET':
        return HttpResponseForbidden()

    # check if user is first time or not and send help msg

    # search the body of message for correct input types
    msg_body = str(request.POST['Body'])
    usr_requested_pkmn_num = number(msg_body)
    if usr_requested_pkmn_num:
        return redirect_to(
            reverse('pokemon-number', args=(usr_requested_pkmn_num,))
        )
    if re.match("^\s*([Aa]bout)\s*$", msg_body):
        return redirect_to(reverse('about'))
    # all gibberish leads to a help redirection
    return redirect_to(reverse('help'))


def pokemon_no(request, num):
    global client
    BASE_URL = 'http://pokeapi.co'
    # check if the number is correct national dex number
    req = requests.get(BASE_URL + '/api/v1/pokemon/' + num + '/')
    if req.status_code != 200:
        return send_sms('That pokemon does not exist.')
    else:   # pokemon exists, send data
        pokemon = req.json()
        # send name data over
        name = pokemon["name"]
        national_id = pokemon['national_id']
        types = ', '.join([typ['name'] for typ in pokemon['types']])
        ability = pokemon['abilities'][0]['name']
        weight = pokemon['weight']
        sprite = BASE_URL + pokemon['sprites'][0]['resource_uri']

        pokemon_info = '\n'.join(
            [name, str(national_id), types, ability, weight]
        )

        response = twilio.twiml.Response()
        response.message(sprite)
        response.message(pokemon_info)
        return HttpResponse(response.toxml(), content_type='text/xml')


def about(request):
    return send_sms('Made by Sooham Rafiz. 2015.\n Thanks to PokeAPI.')


def show_help(request):
    return send_sms('Enter pokemon national dex number to view pokedex entry.')

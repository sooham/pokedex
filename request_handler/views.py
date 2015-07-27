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
PKMN_NAMES = [pokemon['name'] for pokemon in PKMNS]

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
    BASE_URL = 'http://pokeapi.co/api/v1/pokemon/'
    # check if the number is correct national dex number
    request = requests.get(BASE_URL + num + '/')
    if request.status_code != 200:
        if 0 <= num < len(PKMNS):
            # send message for downtime
            send_sms('The PokeAPI is down, please try again later.')
        else:
            send_sms('That pokemon does not exist.')
    else:   # pokemon exists, send data
        send_sms(PKMN_NAMES[num])

    # GET /api/v1/pokemon/ID/
    # Useful keys
    # abilities 0 name
    # national_id
    # evolutions to and evolutions level
    # name
    # wieght
    # total
    # types

    # GET /api/v1/description/ID/
    # description

    # GET /api/v1/sprite/ID
    # image
    client.messages.create(
        to='+16478366256',
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        body='pokemon ' + num
    )
    return HttpResponse()


def about(request):
    return send_sms('Made by Sooham Rafiz. 2015.\n Thanks to PokeAPI.')


def show_help(request):
    return send_sms('Enter pokemon national dex number to view pokedex entry.')

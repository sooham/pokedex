import os

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import TwilioRestClient
import twilio.twiml

client = None


def init_twilio_rest_client():
    global client
    if not client:
        try:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
        except KeyError:
            # not really HttpResponse but
            raise HttpResponseServerError()
        client = TwilioRestClient(account_sid, auth_token)


@csrf_exempt
def index(request):
    global client
    init_twilio_rest_client()
    # search the request body and reply
    # the body back to the sender
    caller = request.POST['From']
    msg_body = request.POST['Body']
    resp = twilio.twiml.Response()
    resp.message(msg_body)
    return HttpResponse(resp.toxml(), content_type='text/xml')


def pokemon_name(request, name):
    global client
    init_twilio_rest_client()
    client.messages.create(
        to='+16478366256',
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        body='pokemon ' + name
    )
    return HttpResponse()


def pokemon_no(request, num):
    global client
    init_twilio_rest_client()
    client.messages.create(
        to='+16478366256',
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        body='pokemon ' + num
    )
    return HttpResponse()


def about(request):
    global client
    init_twilio_rest_client()
    client.messages.create(
        to='+16478366256',
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        body='about page'
    )
    return HttpResponse()

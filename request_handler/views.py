import os

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
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


def index(request):
    global client
    init_twilio_rest_client()
    resp = twilio.twiml.Response()
    resp.message("Hello, mobile monkey")
    return HttpResponse(resp)


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

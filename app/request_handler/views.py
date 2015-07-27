from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


def index(request):
    return HttpResponse("This page should send a general pokedex message")


def pokemon_name(request, name):
    return HttpResponse("Pokedex entry for pokemon %s." % name)


def pokemon_no(request, num):
    return HttpResponse("Pokedex entry for pokemon with dex num %s." % num)


def about(request):
    return HttpResponse("This page should tell the user about the project")

from django.shortcuts import render
from django.http import HttpResponse

def decksView(request):
    return HttpResponse('decks view')

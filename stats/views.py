from django.shortcuts import render
from django.http import HttpResponse

def statsView(request):
    return HttpResponse('stats view')

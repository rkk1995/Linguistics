from django.shortcuts import render
from django.http import HttpResponse

def accountView(request):
    return HttpResponse('account view')

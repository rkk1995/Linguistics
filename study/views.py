from django.shortcuts import render
from django.http import HttpResponse

def studyView(request):
    return HttpResponse('study view')

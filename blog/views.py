from django.shortcuts import render
from django.http import HttpResponse

def blogView(request):
    return HttpResponse('blog view')

def blogArticleView(request):
    return HttpResponse('blog article view')

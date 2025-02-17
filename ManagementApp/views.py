from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


# Create your views here.
def test(request):
    return HttpResponse('Hello, world!')

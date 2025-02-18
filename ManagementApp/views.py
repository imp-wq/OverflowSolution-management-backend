from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
import urllib.parse
import requests



# Create your views here.
def test(request):
    return HttpResponse('Hello, world!')


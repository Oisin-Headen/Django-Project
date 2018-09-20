"""This file contains the url definition"""
from django.http import HttpResponse


def index(request):
    """The Index Page"""
    return HttpResponse("Hello, world. You're at the polls index.")

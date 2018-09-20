"""This file contains the url method definitions"""
from django.http import HttpResponse
from django.template import loader


def index(request):
    """The Index Page"""
    # return HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponse(loader.get_template("paranoidApp/index.html").render({}, request))

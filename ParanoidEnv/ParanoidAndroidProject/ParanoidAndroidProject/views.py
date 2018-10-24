"""This file contains the url method definitions for the entire site"""
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    """Index page for site"""
    HttpResponseRedirect(reverse("paranoidApp:index"))

"""This file contains the url definitions"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

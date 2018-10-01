"""This file contains the url definitions"""
from django.urls import path

from . import views

urlpatterns = [
    path('<int:question_id>', views.index, name='index'),
    path('', views.index, name='index'),
]

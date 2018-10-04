"""This File contains the definitions for the models"""
from django.db import models

# Create your models here.

class Survey(models.Model):
    """Model for the surveys"""
    survey_location = models.CharField(max_length=200)
    answers_location = models.CharField(max_length=200)

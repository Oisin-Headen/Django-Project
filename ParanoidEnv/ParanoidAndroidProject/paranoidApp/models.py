"""This File contains the definitions for the models"""
from django.db import models

# Create your models here.

class Survey(models.Model):
    """Model for the surveys"""
    survey_name = models.CharField(max_length=200)
    survey_desc = models.CharField(max_length=500)

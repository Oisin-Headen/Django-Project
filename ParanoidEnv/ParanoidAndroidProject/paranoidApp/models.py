"""This File contains the definitions for the models"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class SurveyUser(AbstractUser):
    """Users will have their data stored here"""
    is_admin = models.BooleanField(default=False)

class SurveyCreator(models.Model):
    """Info about survey creators"""
    user = models.OneToOneField(SurveyUser, on_delete=models.CASCADE, primary_key=True)

class Survey(models.Model):
    """Model for the surveys"""
    survey_name = models.CharField(max_length=200)
    survey_desc = models.CharField(max_length=500)
    # creator = models.ForeignKey(SurveyCreator, on_delete=models.CASCADE)

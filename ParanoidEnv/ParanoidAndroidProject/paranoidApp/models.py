"""This File contains the definitions for the models"""
from django.db import models

# Create your models here.

class Survey(models.Model):
    """Model for the surveys"""
    survey_desc = models.CharField(max_length=500)
    survey_create_date = models.DateField('date created')

class QuestionType(models.Model):
    """The Question types:
    Free form text,
    Multiple Choice Radio buttons
    Multiple choice checkbox
    """
    question_type_name = models.CharField(max_length=200)

class Question(models.Model):
    """Model for the questions"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200)
    question_desc = models.CharField(max_length=500)
    question_required = models.BooleanField(default=False)

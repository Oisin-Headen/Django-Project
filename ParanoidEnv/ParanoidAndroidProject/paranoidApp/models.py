"""This File contains the definitions for the models"""
from django.db import models

# Create your models here.

class Survey(models.Model):
    """Model for the surveys"""
    survey_desc = models.CharField(max_length=500)
    survey_create_date = models.DateField('date created')

class Question(models.Model):
    """Model for the questions"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200)
    question_desc = models.CharField(max_length=500)
    question_required = models.BooleanField(default=False)

class QuestionType(models.Model):
    """The Question types:
    Free form text,
    Multiple Choice Radio buttons
    Multiple choice checkbox
    Number value
    boolean
    """
    question_type_name = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class BooleanQuestion(QuestionType):
    """Yes or no question"""

class NumericalQuestion(QuestionType):
    """Number Question"""
    min_value = models.IntegerField()
    max_value = models.IntegerField()

class FreeFormQuestion(QuestionType):
    """Free form question"""

class MultipleChoiceRadioQuestion(QuestionType):
    """Radio button Question"""

class MultipleChoiceRadioQuestionAnswer(models.Model):
    """An answer for a radio question"""
    parent_question = models.ForeignKey(MultipleChoiceRadioQuestion, on_delete=models.CASCADE)
    choice_title = models.CharField(max_length=200)

class MultipleChoiceCheckboxQuestion(QuestionType):
    """Checkbox Question"""

class MultipleChoiceCheckboxQuestionAnswer(models.Model):
    """An answer for a checkbox question"""
    parent_question = models.ForeignKey(MultipleChoiceCheckboxQuestion, on_delete=models.CASCADE)
    choice_title = models.CharField(max_length=200)

"""This file contains the url definitions"""
from django.urls import path

from . import views

urlpatterns = [
    path('<int:question_id>', views.index, name='index'),
    path('', views.index, name='index'),
    path('createsurvey/', views.createsurvey, name='createsurvey'),
    path('testpost/', views.testpost, name='testpost'),
    path('view/', views.view_survey, name='view_survey'),
    path('error/', views.error, name='error'),
    path('survey-complete/', views.survey_complete, name='survey_complete'),
    path('post-survey/', views.survey_post_data, name='survey_post_data')
]

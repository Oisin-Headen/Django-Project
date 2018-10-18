"""This file contains the url definitions"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view/<int:survey_id>', views.view_survey, name='view_survey'),
    path('view/', views.view_survey, name='view_survey'),
    path('error/', views.error, name='error'),
    path('view/results', views.survey_complete, name='survey_complete'),
    path('view/response', views.survey_post_data, name='survey_post_data'),
    path('create-survey-single/', views.create_survey, name="create_survey_single"),
    path('create-survey/', views.create_survey_start, name='create_survey'),
    path('create-survey/post/', views.post_create_survey_start, name='create_survey_start'),
    path('create-survey/question-types/', views.create_survey_question_types,
         name='create_survey_question_types'),
    path('create-survey/question-types/post', views.post_create_survey_question_types,
         name='post_create_survey_question_types'),
    path('create-survey/question-types/question-options/', views.create_survey_question_options,
         name='create_survey_question_options'),
    path('create-survey/question-types/question-options/post',
         views.create_survey_question_options_post, name='create_survey_question_options_post'),
    path('survey-created/<int:survey_id>/', views.survey_created, name='survey_created')
]

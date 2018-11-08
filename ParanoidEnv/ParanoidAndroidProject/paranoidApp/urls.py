"""This file contains the url definitions"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view/<int:survey_id>/', views.view_survey, name='view_survey'),
    path('view/', views.view_survey, name='view_survey'),
    path('error/', views.error, name='error'),
    path('view/results', views.survey_complete, name='survey_complete'),
    path('view/response', views.survey_post_data, name='survey_post_data'),

    path('create-survey/', views.create_survey, name="create_survey_single"),
    path('create-survey/post/', views.create_survey_post, name="create_survey_single_post"),
    path('survey-created/<int:survey_id>/', views.survey_created, name='survey_created'),

    path('my-surveys/', views.view_surveys_for_user, name="surveys_for_user"),
    path('my-surveys/<int:survey_id>/', views.view_survey_data, name="survey_data"),

    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),

    path('my-surveys/<int:survey_id>/delete/', views.delete_survey, name="delete_survey"),
    path('survey-deleted/', views.survey_deleted, name="survey_deleted"),

    path('admins/', views.assign_admin_powers, name="assign_admin"),
    path('admins/assign/', views.assign_admin_powers_post, name="assign_admin_post"),

    path('view/analytics', views.analyse_data, name="analyse_data"),
    path('view/<int:survey_id>/analytics', views.analyse_data, name="analyse_data"),
]

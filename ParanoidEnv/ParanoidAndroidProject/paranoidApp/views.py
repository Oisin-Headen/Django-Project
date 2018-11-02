"""This file contains the url method definitions for the app"""
import json
import os
import csv
# import pandas
# import string
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Survey, SurveyCreator
from .forms import SignUpForm

QUESTION_TYPES = {
    "text": "Text",
    "dropdown": "Dropdown",
    "boolean": "Yes or No",
    "radio": "Radio Buttons",
    "number_rating": "Numerical Range",
    "email": "Email",
    "numerical": "Number"
}

def index(request):
    """The Index Page"""
    all_surveys = Survey.objects.all()
    surveys = []
    for survey in all_surveys:
        surveys.append({"id": survey.pk, "name": survey.survey_name})
    return HttpResponse(loader.get_template(
        "paranoidApp/index.html").render({"surveys":surveys}, request))

def view_survey(request, survey_id=-1):
    """View and respond to a survey.
    Currently only views the hard-coded sample survey"""
    if survey_id == -1:
        file_name = "data/survey-1.json"
    else:
        survey = get_object_or_404(Survey, pk=survey_id)
        file_name = "data/survey" + str(survey.pk) + ".json"

    current_folder = os.path.dirname(os.path.abspath(__file__))
    file = open(os.path.join(current_folder, file_name), "r")

    json_data = json.loads(file.read())
    json_data['id'] = survey_id
    survey_data = {"survey":json_data}
    return HttpResponse(loader.get_template("paranoidApp/survey_view.html")
                        .render(survey_data, request))


def process_question(question_input, question):
    """Helper function to process a question"""
    if question_input == "":
        assert question['optional'] is not None, "Didn't answer required question"
        question_value = "NA"

    elif question['type'] == "dropdown" or question['type'] == "radio":
        assert question_input in question['choices'], "Not a valid dropdown choice"
        question_value = '"' + question_input.replace('"', '""') + '"'

    elif question['type'] == "boolean":
        assert question_input in ["Yes", "No"], "Did not answer yes or no"
        question_value = question_input

    elif question['type'] == "text":
        question_value = '"' + question_input.replace('"', '""') + '"'

    elif question['type'] == "number_rating":
        number = question_input
        assert int(question['min']) <= int(number) <= int(question['max']), (
            "Number not in required range: "+str(question['min'])+" - "+str(question['max']))
        question_value = '"' + str(number).replace('"', '""') + '"'

    elif question['type'] == "email":
        question_value = '"' + question_input.replace('"', '""') + '"'

    elif question['type'] == "numerical":
        value = int(question_input)
        if "min" in question.keys():
            assert value >= int(question['min']), "Value below minimum"
        if "max" in question.keys():
            assert value <= int(question['max']), "Value above maximum"

        question_value = str(value)

    else:
        # The type doesn't match, should never happen
        raise AssertionError

    return question_value

@require_POST
def survey_post_data(request):
    """Take the posted data, validate, and store it"""
    try:
        survey_id = request.POST['survey-id']
        # TODO possibly remove the test survey?
        # ^ When test survey is generated on user command and added to the database

        current_folder = os.path.dirname(os.path.abspath(__file__))
        survey_file = os.path.join(current_folder, "data/survey" + str(survey_id) + ".json")
        answers_file = os.path.join(current_folder, "data/survey" + str(survey_id) + ".csv")
        list_entry = "\n"
        survey_stucture = json.loads(open(survey_file, "r").read())

        for i, question in enumerate(survey_stucture['questions'], 1):
            try:
                question_data_input = request.POST[str(survey_id)+"-"+str(i)]
                list_entry += process_question(question_data_input, question)
            except AssertionError as assert_failed:
                messages.add_message(request, messages.ERROR, assert_failed.args[0])
                return HttpResponseRedirect(reverse("error"))

            subquestions = []
            if "subquestions" in question:
                subquestions = question['subquestions']

            if i != len(survey_stucture['questions']) or subquestions:
                list_entry += ","

            for j, subquestion in enumerate(subquestions, 1):
                subquestion_input = request.POST[str(survey_id)+"-"+str(i)+"-"+str(j)]

                if question['on']:
                    if (question_data_input == "Yes" and question['on'] is False
                       ) or (question_data_input == "No" and question['on'] is True):
                        list_entry += "NA"

                    else:
                        try:
                            list_entry += process_question(subquestion_input, subquestion)
                        except AssertionError as assert_failed:
                            messages.add_message(request, messages.ERROR, str(assert_failed))
                            return HttpResponseRedirect("error")
                else:
                    messages.add_message(
                        request, messages.ERROR, 
                        "Error: this boolean question has a subquestions field without an on field")
                    return HttpResponseRedirect("error")

                if i != len(survey_stucture['questions']) or j != len(question['subquestions']):
                    list_entry += ","

        data_file = open(answers_file, "a")
        data_file.write(list_entry)
        data_file.close()
        return HttpResponseRedirect(reverse("survey_complete"))

    except KeyError as key_error:
        messages.add_message(request, messages.ERROR, "A field could not be accessed: " + str(
            key_error.args[0]))
        return HttpResponseRedirect(reverse("error"))


def error(request):
    """An error occured somewhere"""
    # error_message = request.session['error_message']
    return HttpResponse(loader.get_template("paranoidApp/error.html").render({}, request))

def survey_complete(request):
    """The survey was completed succsessfully"""
    return HttpResponse(loader.get_template("paranoidApp/survey_complete.html").render({}, request))

@login_required
def create_survey(request):
    """Create survey from a single page"""
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_single_page.html")
                        .render({}, request))

def validate_questions(json_data):
    """Handles possible validation of questions"""
    assert json_data['name'], "No name provided"
    assert json_data['desc'], "No description provided"
    for question in json_data['questions']:
        assert question['text'], "No text for question provided"
        assert question['column-name'], "No name for question provided"
        assert question['type'] in QUESTION_TYPES, "Question type does not exist"
        if question['type'] == "number_rating":
            assert int(question['max']) > int(question['min']), "Max is less than min"
        elif question['type'] == "numerical":
            if('max' in question.keys() and 'min' in question.keys()):
                assert int(question['max']) > int(question['min']), "Max is less than min"
        elif question['type'] == "dropdown" or question['type'] == "radio":
            assert question['choices'], "No choices provided"
        elif question['type'] == "boolean":
            if "on" in question.keys():
                assert question['on'] in ["true", "false"], "On field must be true or false"
                # correcting this value to boolean, rather than text
                question['on'] = question['on'] == "true"
                assert question['subquestions'], "No subquestions provided"
                for subquestion in question['subquestions']:
                    assert subquestion['text'], "No text for subquestion provided"
                    assert subquestion['column-name'], "No name for subquestion provided"
                    assert subquestion['type'] in QUESTION_TYPES, "Question type does not exist"
                    if subquestion['type'] == "number_rating":
                        assert (int(subquestion['max']) <
                                int(subquestion['min'])), "Max is less than min"
                    elif subquestion['type'] == "numerical":
                        if('max' in subquestion.keys() and 'min' in subquestion.keys()):
                            assert int(subquestion['max']) > int(
                                subquestion['min']), "Max is less than min"
                    elif (subquestion['type'] == "dropdown" or
                          subquestion['type'] == "radio"):
                        assert subquestion['choices'], "No choices provided"

@login_required
@require_POST
def create_survey_post(request):
    """Post request for creating survey"""
    json_data = json.loads(request.POST['json'])
    try:
        validate_questions(json_data)
    except KeyError as error_here:
        messages.add_message(request, messages.ERROR, "A field could not be accessed: " + str(
            error_here.args[0]))
        return HttpResponseRedirect(reverse("error"))
    except AssertionError as assertion_error:
        messages.add_message(request, messages.ERROR, "Something went wrong: " + str(
            assertion_error.args[0]))
        return HttpResponseRedirect(reverse("error"))

    database_entry = Survey(survey_name=json_data['name'],
                            survey_desc=json_data['desc'],
                            creator=SurveyCreator.objects.get(user=request.user.id))
    database_entry.save()
    survey_id = database_entry.pk

    current_folder = os.path.dirname(os.path.abspath(__file__))
    survey_file = os.path.join(current_folder, "data/survey"+str(survey_id)+".json")
    answers_file = os.path.join(current_folder, "data/survey"+str(survey_id)+".csv")
    json_data_string = json.dumps(json_data, indent=4)


    survey_file_writing = open(survey_file, "w+")
    survey_file_writing.write(json_data_string)
    survey_file_writing.close()

    csv_header = ""
    for question in json_data['questions']:
        csv_header += ('"'+question['column-name'].replace('"', '""')+'",')
        if 'subquestions' in question.keys():
            for subquestion in question['subquestions']:
                csv_header += ('"'+subquestion['column-name'].replace('"', '""')+'",')
    csv_header = csv_header[:-1]
    answers_file_writing = open(answers_file, "w+")
    answers_file_writing.write(csv_header)
    answers_file_writing.close()

    return HttpResponseRedirect(reverse("survey_created", kwargs={"survey_id": survey_id}))

def survey_created(request, survey_id):
    """Survey has been created"""
    survey = Survey.objects.get(pk=survey_id)
    return HttpResponse(loader.get_template("paranoidApp/survey_created.html")
                        .render({"surveyname":survey.survey_name,
                                 "surveydesc": survey.survey_desc}, request))

@login_required
def view_surveys_for_user(request):
    """View a user's survey"""
    surveys = Survey.objects.filter(creator=request.user.id)
    return HttpResponse(loader.get_template("paranoidApp/user_surveys.html")
                        .render({"surveys": surveys}, request))

@login_required
def view_survey_data(request, survey_id):
    """View the responses for the survey"""
    survey = get_object_or_404(Survey, pk=survey_id)
    if survey.creator != request.user.id and not request.user.is_admin:
        HttpResponseRedirect(reverse('error'))
    current_folder = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(current_folder, "data/survey" + str(survey_id) + ".csv")
    file = open(file_name, "r")
    csv_data = []
    csv_reader = csv.reader(file)
    for row in csv_reader:
        csv_data.append(row)
    file.close()

    return HttpResponse(loader.get_template("paranoidApp/survey_data.html")
                        .render({"data": csv_data}, request))

def signup(request):
    """The Signup form"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            creator = SurveyCreator(user=user)
            creator.save()
            login(request, user)
            return redirect(reverse("index"))
    else:
        form = SignUpForm()
    return render(request, 'paranoidApp/signup.html', {'form': form})

def logout(request):
    """Logs a user out"""
    django_logout(request)
    return HttpResponseRedirect(reverse("index"))

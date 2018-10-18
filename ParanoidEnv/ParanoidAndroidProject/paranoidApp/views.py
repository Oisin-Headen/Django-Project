"""This file contains the url method definitions"""
import json
# import pandas
# import string
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Survey

QUESTION_TYPES = {
    "text": "Text",
    "single_answer_multiple_choice": "Dropdown",
    "boolean": "Yes or No",
    "scale": "Radio Buttons",
    "number_rating": "Numerical",
    "email": "Email"
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
        file = open("data/surveydata.json", "r")
    else:
        survey = get_object_or_404(Survey, pk=survey_id)
        file = open("data/survey" + str(survey.pk) + ".json", "r")
    json_data = json.loads(file.read())
    json_data['id'] = survey_id
    survey_data = {"survey":json_data}
    return HttpResponse(loader.get_template("paranoidApp/survey_view.html")
                        .render(survey_data, request))

# TODO Split up this function, currently spaghetti code
def survey_post_data(request):
    """Take the posted data, validate, and store it"""
    try:
        postdata = request.POST
        survey_id = postdata['survey-id']
        # TODO possibly remove this test survey?
        if int(survey_id) == -1:
            survey_file = "data/surveydata.json"
            answers_file = "data/surveydata.csv"
        else:
            survey_file = "data/survey" + str(survey_id) + ".json"
            answers_file = "data/survey" + str(survey_id) + ".csv"
        list_entry = "\n"
        error_occured = False
        survey_stucture = json.loads(open(survey_file, "r").read())

        for i, question in enumerate(survey_stucture['questions'], 1):
            if postdata[str(survey_id)+"-"+str(i)] == "":
                list_entry += "NA"

            elif question['type'] == "single_answer_multiple_choice":
                if postdata[str(survey_id)+"-"+str(i)] in question['choices']:
                    list_entry += postdata[str(survey_id)+"-"+str(i)]
                else:
                    error_occured = True
                    print("single_answer_multiple_choice error")
                    break

            elif question['type'] == "scale":
                if postdata[str(survey_id)+"-"+str(i)] in question['choices']:
                    list_entry += postdata[str(survey_id)+"-"+str(i)]
                else:
                    error_occured = True
                    print("scale error")
                    break

            elif question['type'] == "boolean":
                if postdata[str(survey_id)+"-"+str(i)] == "Yes":
                    list_entry += "Yes"
                elif postdata[str(survey_id)+"-"+str(i)] == "No":
                    list_entry += "No"
                else:
                    error_occured = True
                    print("boolean error")
                    break

            elif question['type'] == "text":
                list_entry += '"' + postdata[str(survey_id)+"-"+str(i)].replace('"', '""') + '"'

            elif question['type'] == "number_rating":
                number = postdata[str(survey_id)+"-"+str(i)]
                if question['min'] <= int(number) <= question['max']:
                    list_entry += str(number)
                else:
                    error_occured = True
                    print("number_rating error")
                    break

            elif question['type'] == "email":
                list_entry += '"' + postdata[str(survey_id)+"-"+str(i)].replace('"', '""') + '"'

            else:
                error_occured = True
                break

            subquestions = []
            if "subquestions" in question:
                subquestions = question['subquestions']

            if i != len(survey_stucture['questions']) or subquestions:
                list_entry += ","

            for j, subquestion in enumerate(subquestions, 1):
                if postdata[str(survey_id)+"-"+str(i)+"-"+str(j)] == "":
                    list_entry += "NA"
                    if i != len(survey_stucture['questions']) or j != len(question['subquestions']):
                        list_entry += ","
                    continue

                if question['on']:
                    if (postdata[str(survey_id)+"-"+str(i)] == "Yes" and question['on'] is False
                       ) or (postdata[str(survey_id)+"-"+str(i)] == "No" and question['on'] is True):
                        list_entry += "NA"
                        if i != len(survey_stucture['questions']) or j != len(question['subquestions']):
                            list_entry += ","
                        continue

                if subquestion['type'] == "scale":
                    if postdata[str(survey_id)+"-"+str(i)+"-"+str(j)] in subquestion['choices']:
                        list_entry += postdata[str(survey_id)+"-"+str(i)+"-"+str(j)]
                    else:
                        error_occured = True
                        break

                elif subquestion['type'] == "boolean":
                    if postdata[str(survey_id)+"-"+str(i)+"-"+str(j)] == "Yes":
                        list_entry += "Yes"
                    elif postdata[str(survey_id)+"-"+str(i)+"-"+str(j)] == "No":
                        list_entry += "No"
                    else:
                        error_occured = True
                        break

                elif subquestion['type'] == "text":
                    list_entry += '"' + postdata[str(survey_id)+"-"+str(i)+"-"+str(j)].replace('"', '""') + '"'

                elif subquestion['type'] == "number_rating":
                    number = postdata[str(survey_id)+"-"+str(i)+"-"+str(j)]
                    if subquestion['min'] <= int(number) <= subquestion['max']:
                        list_entry += str(number)
                    else:
                        error_occured = True
                        break

                elif subquestion['type'] == "email":
                    list_entry += '"' + postdata[str(survey_id)+"-"+str(i)+"-"+str(j)].replace('"', '""') + '"'

                else:
                    error_occured = True
                    break

                if i != len(survey_stucture['questions']) or j != len(question['subquestions']):
                    list_entry += ","

        if error_occured:
            return HttpResponseRedirect(reverse("error"))

        data_file = open(answers_file, "a")
        data_file.write(list_entry)
        data_file.close()
        return HttpResponseRedirect(reverse("survey_complete"))

    except KeyError:
        return HttpResponseRedirect(reverse("error"))


def error(request):
    """An error occured somewhere"""
    return HttpResponse(loader.get_template("paranoidApp/error.html").render({}, request))

def survey_complete(request):
    """The survey was completed succsessfully"""
    # dataframe = pandas.read_csv('data/surveydata.csv')
    # print(dataframe.describe())
    return HttpResponse(loader.get_template("paranoidApp/survey_complete.html").render({}, request))

def create_survey(request):
    """Create survey from a single page"""
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_single_page.html")
                        .render({}, request))

def create_survey_start(request):
    """Sends back the survey title, description, and the number of questions in the survey"""
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_num_questions.html")
                        .render({}, request))

def post_create_survey_start(request):
    """The survey creation form posts here"""
    postdata = request.POST
    new_survey = {
        'name': postdata['name'],
        'desc': postdata['desc']
    }
    request.session['new_survey'] = new_survey
    request.session['new_survey_num_questions'] = postdata['number_of_questions']
    return HttpResponseRedirect(reverse('create_survey_question_types'))

def create_survey_question_types(request):
    """Allow the user to choose a question type per question"""
    data = {
        "survey_name": request.session['new_survey']['name'],
        "number_questions": range(1, 1 + int(request.session['new_survey_num_questions']))
    }
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_question_types.html")
                        .render(data, request))

def post_create_survey_question_types(request):
    """Process the user's question type choices"""
    request.session['new_survey']['questions'] = []
    for i in range(1, 1 + int(request.session['new_survey_num_questions'])):
        if request.POST['Q'+str(i)] in QUESTION_TYPES.keys():
            question = {
                "type": request.POST['Q'+str(i)]
            }
            request.session['new_survey']['questions'].append(question)
        else:
            # TODO Throw an error!
            pass
    request.session.modified = True
    return HttpResponseRedirect(reverse('create_survey_question_options'))

def create_survey_question_options(request):
    """Allow the user to customize the questions"""
    questions_data = []
    for question in request.session['new_survey']['questions']:
        question_data = {
            "type_name": QUESTION_TYPES[question['type']],
            "type": question['type']
        }
        questions_data.append(question_data)
    data = {
        "questions": questions_data,
        "name": request.session['new_survey']['name']
    }
    print(request.session['new_survey']['questions'])
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_question_options.html")
                        .render(data, request))

def create_survey_question_options_post(request):
    """Finalize survey"""
    try:
        for i, question in enumerate(request.session['new_survey']['questions'], 1):
            question['column-name'] = request.POST['Q'+str(i)+'-title']
            question['text'] = request.POST['Q'+str(i)+'-text']
            if question['type'] == "scale" or question['type'] == "single_answer_multiple_choice":
                choices = [
                    request.POST['Q'+str(i)+"-choice1"],
                    request.POST['Q'+str(i)+"-choice2"],
                    request.POST['Q'+str(i)+"-choice3"]
                ]
                question['choices'] = choices
            elif question['type'] == "number_rating":
                question['max'] = int(request.POST['Q'+str(i)+"-max"])
                question['min'] = int(request.POST['Q'+str(i)+"-min"])
    except KeyError:
        return HttpResponseRedirect(reverse("error"))

    # print(request.session['new_survey'])

    database_entry = Survey(survey_name=request.session['new_survey']['name'],
                            survey_desc=request.session['new_survey']['desc'])
    database_entry.save()
    survey_id = database_entry.pk
    survey_file = "data/survey"+str(survey_id)+".json"
    answers_file = "data/survey"+str(survey_id)+".csv"
    json_data = json.dumps(request.session['new_survey'], indent=4)

    survey_file_writing = open(survey_file, "w+")
    survey_file_writing.write(json_data)
    survey_file_writing.close()

    answers_file_writing = open(answers_file, "w+")
    csv_header = ""
    for question in request.session['new_survey']['questions']:
        csv_header += ('"'+question['column-name'].replace('"', '""')+'",')
        if 'subquestions' in question.keys():
            for subquestion in question['subquestions']:
                csv_header += ('"'+subquestion['column-name'].replace('"', '""')+'",')
    answers_file_writing.write(csv_header)
    answers_file_writing.close()

    # del request.session['new_survey']
    # del request.session['new_survey_num_questions']
    return HttpResponseRedirect(reverse("survey_created", kwargs={"survey_id": survey_id}))


def survey_created(request, survey_id):
    """Survey has been created"""
    survey = Survey.objects.get(pk=survey_id)
    return HttpResponse(loader.get_template("paranoidApp/survey_created.html")
                        .render({"surveyname":survey.survey_name, 
                                "surveydesc": survey.survey_desc}, request))

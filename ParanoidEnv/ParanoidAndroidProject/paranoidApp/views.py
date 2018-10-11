"""This file contains the url method definitions"""
import json
import pandas
# import string
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Survey

question_types = [
    "text",
    "single_answer_multiple_choice",
    "boolean",
    "scale",
    "number_rating",
    "email"
]

def index(request):
    """The Index Page"""
    all_surveys = Survey.objects.all()
    surveys = []
    for survey in all_surveys:
        surveys.append({"id": survey.pk, "name": survey.survey_name})
    return HttpResponse(loader.get_template(
        "paranoidApp/index.html").render({"surveys":surveys}, request))

def view_survey(request):
    """View and respond to a survey.
    Currently only views the hard-coded sample survey"""
    file = open("data/surveydata.json", "r")
    json_data = json.loads(file.read())
    json_data['id'] = 1
    survey_data = {"survey":json_data}
    return HttpResponse(loader.get_template("paranoidApp/survey_view.html")
                        .render(survey_data, request))

# TODO Split up this function, currently spaghetti code
def survey_post_data(request):
    """Take the posted data, validate, and store it"""
    try:
        postdata = request.POST
        survey_id = postdata['survey-id']
        # TODO get data filename from id
        survey_file = "data/surveydata.json"
        answers_file = "data/surveydata.csv"
        list_entry = "\n"
        error_occured = False
        survey_stucture = json.loads(open(survey_file, "r").read())
        # pdb.set_trace()
        for i, question in enumerate(survey_stucture['questions'], 1):
            if postdata[str(survey_id)+"-"+str(i)] == "":
                list_entry += "NaN"

            elif question['type'] == "single_answer_multiple_choice":
                if postdata[str(survey_id)+"-"+str(i)] in question['choices']:
                    list_entry += postdata[str(survey_id)+"-"+str(i)]
                else:
                    error_occured = True
                    break

            elif question['type'] == "scale":
                if postdata[str(survey_id)+"-"+str(i)] in question['choices']:
                    list_entry += postdata[str(survey_id)+"-"+str(i)]
                else:
                    error_occured = True
                    break

            elif question['type'] == "boolean":
                if postdata[str(survey_id)+"-"+str(i)] == "Yes":
                    list_entry += "Yes"
                elif postdata[str(survey_id)+"-"+str(i)] == "No":
                    list_entry += "No"
                else:
                    error_occured = True
                    break

            elif question['type'] == "text":
                # TODO test this sanitization (for csv)
                list_entry += '"' + postdata[str(survey_id)+"-"+str(i)].replace('"', '""') + '"'

            elif question['type'] == "number_rating":
                number = postdata[str(survey_id)+"-"+str(i)]
                if question['min'] <= int(number) <= question['max']:
                    list_entry += str(number)
                else:
                    error_occured = True
                    break

            elif question['type'] == "email":
                # TODO test this sanitization (for csv)
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
                    list_entry += "NaN"

                elif subquestion['type'] == "scale":
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
                    # TODO test this sanitization (for csv)
                    list_entry += '"' + postdata[str(survey_id)+"-"+str(i)+"-"+str(j)].replace('"', '""') + '"'

                elif subquestion['type'] == "number_rating":
                    number = postdata[str(survey_id)+"-"+str(i)+"-"+str(j)]
                    if subquestion['min'] <= int(number) <= subquestion['max']:
                        list_entry += str(number)
                    else:
                        error_occured = True
                        break

                elif subquestion['type'] == "email":
                    # TODO test this sanitization (for csv)
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
    dataframe = pandas.read_csv('data/surveydata.csv')
    print(dataframe.describe())
    return HttpResponse(loader.get_template("paranoidApp/survey_complete.html").render({}, request))



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
        "number_questions": range(1, int(request.session['new_survey_num_questions']))
    }
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_question_types.html")
                        .render(data, request))

def post_create_survey_question_types(request):
    """Process the user's question type choices"""
    request.session['new_survey']['questions'] = []
    for i in range(1, int(request.session['new_survey_num_questions'])):
        if request.POST['Q'+str(i)] in question_types:
            question = {
                "type": request.POST['Q'+str(i)]
            }
            request.session['new_survey']['questions'].append(question)
        else:
            # TODO Throw an error!
            pass
    return HttpResponseRedirect(reverse('create_survey_question_options'))

def create_survey_question_options(request):
    """Allow the user to customize the questions"""
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_question_options.html")
                        .render({}, request))

def create_survey_question_options_post(request):
    """Finalize survey"""


def survey_created(request, survey_id):
    """Survey has been created"""
    survey = Survey.objects.get(pk=survey_id)
    return HttpResponse(loader.get_template("paranoidApp/survey_created.html").render({"surveyname":survey.survey_name, "surveydesc": survey.survey_desc}, request))



# Survey creation
# Post data comes in,
# string starts: '{"survey":['
# foreach question
#   append "<counter>:
#       {
#           type:<question_type>
#           desc:<description>
#           <[other_details]>
#       },"
# string ends: ']}'

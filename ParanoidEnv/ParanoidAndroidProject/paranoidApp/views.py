"""This file contains the url method definitions"""
import json
import pandas
# import string
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

def index(request):
    """The Index Page"""
    return HttpResponse(loader.get_template("paranoidApp/index.html").render({}, request))

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

def createsurvey(request):
    """Testing post currently"""
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_form.html")
                        .render({}, request))

def post_create_survey(request):
    """The survey creation form posts here"""
    postdata = request.POST

    return HttpResponseRedirect(reverse("survey_created"))

def survey_created(request):
    """Survey has been created"""
    return HttpResponse(loader.get_template("paranoidApp/survey_created.html").render({}, request))


def view_survey(request):
    """View and respond to a survey.
    Currently only views the hard-coded sample survey"""
    file = open("data/surveydata.json", "r")
    json_data = json.loads(file.read())
    json_data['id'] = 1
    survey_data = {"survey":json_data}
    return HttpResponse(loader.get_template("paranoidApp/survey_view.html")
                        .render(survey_data, request))

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

"""This file contains the url method definitions"""
import json
from django.http import HttpResponse
from django.template import loader



# def index(request):
#     """The Index Page"""
#     # return HttpResponse("Hello, world. You're at the polls index.")
#     return HttpResponse(loader.get_template("paranoidApp/index.html").render({}, request))

def index(request, question_id=-1):
    """The Index Page, with a survey id"""
    if question_id == 1:
        context = {'status': "valid"}
    else:
        context = {'status': "invalid"}
    return HttpResponse(loader.get_template("paranoidApp/index.html").render(context, request))

def testjson(request):
    """Testing json files and file reading"""
    data = {
        "first": "What is your name",
        "second": "What is your quest?",
        "third": "What is your favourite colour?"
    }
    file = open("data/test.json", "w+")
    file.write(json.dumps(data, indent=4))
    file.close()
    return HttpResponse(loader.get_template("paranoidApp/index.html").render({}, request))

def testpost(request):
    """Testing post data"""
    try:
        postdata = request.POST
    except KeyError:
        pass
    else:
        return HttpResponse(loader.get_template("paranoidApp/survey_complete.html")
                            .render({"text":postdata}, request))

def createsurvey(request):
    """Testing post currently"""
    return HttpResponse(loader.get_template("paranoidApp/survey_creation_form.html")
                        .render({}, request))

def view_survey(request):
    """View and respond to a survey.
    Currently only views the hard-coded sample survey"""
    file = open("data/surveydata.json", "r")
    json_data = json.loads(file.read())
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


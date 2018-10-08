"""This file contains the url method definitions"""
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def index(request):
    """The Index Page"""
    return HttpResponse(loader.get_template("paranoidApp/index.html").render({}, request))

def survey_post_data(request):
    """Take the posted data, validate, and store it"""
    try:
        postdata = request.POST
    except KeyError:
        pass
    else:
        survey_id = postdata['survey_id']
        # TODO get data filename from id
        file_name = "surveydata"
        list_entry = ""
        error = False
        survey_stucture = json.loads(open(file_name+".json", "r").readlines())
        for i, question in enumerate(survey_stucture['questions'], 1):
            if postdata[survey_id+"-"+i] == "":
                    list_entry += "NA"

            elif question['type'] == "scale":
                if question['choices'].contains(postdata[survey_id+"-"+i]):
                    list_entry += postdata[survey_id+"-"+i]
                else:
                    error = True
                    break

            elif question['type'] == "boolean":
                if postdata[survey_id+"-"+i] == "Yes":
                    list_entry += "True,"
                elif postdata[survey_id+"-"+i] == "No":
                    list_entry += "False,"
                else:
                    error = True
                    break

            elif question['type'] == "text":
                # TODO sanitize this input
                list_entry += postdata[survey_id+"-"+i]

            elif question['type'] == "number_rating":
                number = postdata[survey_id+"-"+i]
                if question['min'] <= number <= question['max']:
                    list_entry += number+","
                else:
                    error = True
                    break

            elif question['type'] == "email":
                # TODO sanitize this input
                list_entry += postdata[survey_id+"-"+i]

            else:
                error = True
                break


            for j, subquestion in enumerate(question['subquestions']):
                if postdata[survey_id+"-"+i+"-"+j] == "":
                    list_entry += "NA"
                
                elif subquestion['type'] == "scale":
                    if subquestion['choices'].contains(postdata[survey_id+"-"+i+"-"+j]):
                        list_entry += postdata[survey_id+"-"+i+"-"+j]
                    else:
                        error = True
                        break

                elif subquestion['type'] == "boolean":
                    if postdata[survey_id+"-"+i+"-"+j] == "Yes":
                        list_entry += "True,"
                    elif postdata[survey_id+"-"+i+"-"+j] == "No":
                        list_entry += "False,"
                    else:
                        error = True
                        break
                        
                elif question['type'] == "text":
                    # TODO sanitize this input
                    list_entry += postdata[survey_id+"-"+i+"-"+j]

                elif subquestion['type'] == "number_rating":
                    number = postdata[survey_id+"-"+i+"-"+j]
                    if subquestion['min'] <= number <= subquestion['max']:
                        list_entry += number+","
                    else:
                        error = True
                        break

                elif subquestion['type'] == "email":
                    # TODO sanitize this input
                    list_entry += postdata[survey_id+"-"+i+"-"+j]

        if error:
            return HttpResponseRedirect("survey_error")


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

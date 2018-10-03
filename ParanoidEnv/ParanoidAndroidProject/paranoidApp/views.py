"""This file contains the url method definitions"""
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
    file = open("data/test.json", "w+")
    file.write('{"first": "What is your name", "second": "What is your quest?",'+
               '"third": "What is your favourite colour?"}')
    file.close()
    return HttpResponse(loader.get_template("paranoidApp/index.html").render({}, request))

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

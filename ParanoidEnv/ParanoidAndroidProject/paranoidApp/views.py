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

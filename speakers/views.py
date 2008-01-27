# Create your views here.
from django.shortcuts import render_to_response
from common.models import *
from common.forms import *
from django.http import HttpRequest
def index(request):
    isinstance(request,HttpRequest)
    if request.POST != None:
        pf = PresenterForm(request.POST)
        if pf.is_valid():
            
        
    else :
        return render_to_response('call_for_papers.html',None)
    
def saveSubmission(request):
    return render_to_response('call_for_papers.html',None)
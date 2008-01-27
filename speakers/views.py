# Create your views here.
from django.shortcuts import render_to_response
from common.models import *
from common.forms import *
from django.http import HttpRequest
def index(request):
    isinstance(request,HttpRequest)
    pf = PresenterForm()
    if request.POST != None:
        pf = PresenterForm(request.POST)
        if not pf.is_valid():
             return render_to_response('call_for_papers.html',{'presentation_form':pf})
        else:
            
    else :
        return render_to_response('call_for_papers.html',{'presentation_form':pf})
    
def submitted(request):
    return render_to_response('call_for_papers.html',None)
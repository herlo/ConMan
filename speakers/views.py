# Create your views here.
from django.shortcuts import render_to_response
from common.models import *
from common.forms import *

def index(request):
    return render_to_response('call_for_papers.html',None)
    
def
# Create your views here.
from django.shortcuts import render_to_response
from common.models import *

def index(request):
    
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})


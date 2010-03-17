# Create your views here.

from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse

def index(request):
    return render_to_response('ticketing/index.html', context_instance=RequestContext(request))
 

# Create your views here.

from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.contrib.sites.models import Site

from models import Ticket,Event

def index(request):

    if request.method == 'POST':
        pass
    else:
        current_site = Site.objects.get_current()
        event = Event.objects.get(site=current_site)

    return render_to_response('ticketing/index.html', { 'event': event }, context_instance=RequestContext(request))

def event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render_to_response('ticketing/ticket.html', {
        'event': event
    })

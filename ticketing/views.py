# Create your views here.

from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.contrib.sites.models import Site

from event.models import Event,EventDay
from forms import TicketQtyForm

def index(request):
    current_site = Site.objects.get_current()
    event = Event.objects.get(site=current_site)
    event_days = event.eventday_set.all()
    event_logo = event.logo.name.split('/')[-2] + "/" + event.logo.name.split('/')[-1]

    tickets = event.ticket_set.all()
    form = TicketQtyForm(request.POST or None, tickets=tickets)
    if form.is_valid():
        request.session['tickets'] = []
        for (ticket, qty) in form.tickets():
            if int(qty) > 0:
                print ticket, qty
                request.session['tickets'].append((ticket,qty))
        return HttpResponseRedirect('/tickets/item')

    return render_to_response('ticketing/ticket.html', {
        'event': event,
        'event_days': event_days,
        'event_logo': event_logo,
        'form': form,
        'tickets': tickets
    }, context_instance=RequestContext(request))

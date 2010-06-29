# Create your views here.

from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.contrib.sites.models import Site

from cart import Cart
from paypal.standard.forms import PayPalPaymentsForm

from event.models import Event,EventDay
from ticketing.models import Ticket, Item
from forms import TicketQtyForm, ItemQtyForm

def index(request):
    current_site = Site.objects.get_current()
    event = Event.objects.get(site=current_site)
    event_days = event.eventday_set.all()
    event_logo = event.logo.name.split('/')[-2] + "/" + event.logo.name.split('/')[-1]

    tickets = event.ticket_set.all()
    form = TicketQtyForm(request.POST or None, tickets=tickets)
    if form.is_valid():
        cart = Cart(request)
        for (ticket, qty) in form.tickets():
            if qty > 0:
                ticket = Ticket.objects.get(id=ticket)
                cart.add(ticket, ticket.price, qty)
        if event.item_set.all():
            return HttpResponseRedirect('/tickets/items')
        else:
            return HttpResponseRedirect('/tickets/cart')

    return render_to_response('ticketing/ticket.html', {
        'event': event,
        'event_days': event_days,
        'event_logo': event_logo,
        'form': form,
        'tickets': tickets
    }, context_instance=RequestContext(request))

def items(request):
    current_site = Site.objects.get_current()
    event = Event.objects.get(site=current_site)
    event_days = event.eventday_set.all()
    event_logo = event.logo.name.split('/')[-2] + "/" + event.logo.name.split('/')[-1]

    items = event.item_set.all()
    form = ItemQtyForm(request.POST or None, items=items)
    if form.is_valid():
        cart = Cart(request)
        for (item, qty) in form.items():
            if qty > 0:
                item = Item.objects.get(id=item)
                cart.add(item, item.price, qty)
        return HttpResponseRedirect('/tickets/cart')

    return render_to_response('ticketing/items.html', {
        'event': event,
        'event_days': event_days,
        'event_logo': event_logo,
        'form': form,
        'items': items,
        'cart': Cart(request),
    }, context_instance=RequestContext(request))

def delete(request, id):
    cart = Cart(request)
    cart.delete_item(id)
    return HttpResponseRedirect('/tickets/cart')


def cart(request):
    cart = Cart(request)
    paypal_dict = {
        "business": "utos.org",
        "amount": cart.total_price,
        "item_name": "UTOS 2010 Registration",
        "invoice": "unique-invoice-id",
        "notify_url": "http://www.example.com/your-ipn-location/",
        "return_url": "http://www.example.com/your-return-location/",
        "cancel_return": "http://www.example.com/your-cancel-location/",
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        "form": form,
        'cart': cart,
    }
    return render_to_response('ticketing/cart.html', context, context_instance=RequestContext(request))

from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse

from sponsors.models import Level, Sponsor
# Create your views here.

def index(request):
    sponsors = Sponsor.objects.all().order_by('-level__order')
    return render_to_response('show_sponsors.html', {'sponsors': sponsors}, context_instance=RequestContext(request))

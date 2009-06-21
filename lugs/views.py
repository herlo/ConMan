from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse

from lugs.models import Type, LUG
# Create your views here.

def index(request):
    lugs = Sponsor.objects.all().order_by('-type__order')
    return render_to_response('show_sponsors.html', {'lugs': lugs}, context_instance=RequestContext(request))

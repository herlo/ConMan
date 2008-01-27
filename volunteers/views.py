# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse 
from common.models import Volunteer, UserProfile
from common.forms import VolunteerForm
from django.shortcuts import render_to_response


def index(request):
    form = VolunteerForm()
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            v = Volunteers.objects.create(role=VolunteerRole.objects.create(name=form.name), 
            request=VolunteerRole(name=form.requested_role), 
            comments=form.comments)
            HttpResponseRedirect(reverse(conman.common.views.accepted, args=(v.id)))
        else:
            return render_to_response('volunteer_template.html',{'volunteer_form':form} )
    return render_to_response('call_for_volunteers.html' )

def post(request):
    form = VolunteerForm(request.POST)
    if form.is_valid():
        v = Volunteers.objects.create(role=VolunteerRole.objects.create(name=form.name), 
        request=VolunteerRole(name=form.requested_role), 
        comments=form.comments)
        HttpResponseRedirect(reverse(conman.common.views.accepted, args=(v.id)))
    else:
        return render_to_response('volunteer_template.html',{'volunteer_form':form} )


def accepted(request, v_id):
    vol = get_object_or_404(Volunteer, pk=v_id)
    return render_to_response('volunteer_accepted.html', {'vol_info': vol})

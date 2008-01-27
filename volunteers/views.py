# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse 
from django.shortcuts import render_to_response
from common.models import Volunteer, UserProfile, VolunteerRole
from common.forms import VolunteerForm

def index(request):
    form = VolunteerForm()
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            v = Volunteer.objects.create(role=VolunteerRole.objects.create(name=form.data['username']), 
            request=VolunteerRole.objects.get(id=form.data['requested_role']), 
            comments=form.data['comments'])

            return render_to_response('volunteer_submitted.html')
            #return HttpResponseRedirect(reverse('conman.common.views.submitted', args=(p.id,)))
        else:
            return render_to_response('call_for_volunteers.html', {'volunteers_form': form} )
    else:
        return render_to_response('call_for_volunteers.html',{'volunteers_form':form} )

def submitted(request, v_id):
    v = get_object_or_404(Volunteer, pk=v_id)
    return render_to_response('volunteer_submitted.html', {'volunteers_info': v})

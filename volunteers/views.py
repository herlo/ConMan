# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
from conman.common.models import Volunteer, UserProfile
from conman.common.forms import VolunteerForm

def index(request):
    form = VolunteerForm(request.POST)
    if form.is_valid():
        v = Volunteers.objects.create(role=VolunteerRole.objects.create(name=form.name), 
        request=VolunteerRole(name=form.requested_role), 
        comments=form.comments)
        HttpResponseRedirect(reverse(conman.common.views.accepted, args=(v.id)))
    else:
        return render_to_response('common/volunteer_template.html' )

def accepted(request, v_id):
    vol = get_object_or_404(Volunteer, pk=v_id)
    return render_to_response('common/volunteer_accepted.html', {'vol_info': vol})

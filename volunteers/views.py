from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required

from volunteers.models import Volunteer
from volunteers.forms import VolunteerForm

# Create your views here.
@login_required
def index(request):
    # First we need to check if the user has already submitted a request and 
    # if so we check to see if a role has been assigned.  If one has not we
    # notify them that their request has already been processed but not 
    # decision has been made.  If a role has been assigned we display it.
    volunteer_existed = False
    profile = request.user.get_profile()

    try:
        instance = Volunteer.objects.get(volunteer=profile)
        volunteer_existed = True
    except Volunteer.DoesNotExist:
        instance = profile

    if request.method == 'POST':
        vf = VolunteerForm(request.POST, instance=instance)
        if vf.is_valid():
            # not as elegant as I'd prefer...  there's gotta be a better way
            page = "volunteer_submitted.html"
            v = Volunteer()
            if volunteer_existed:
                v = instance
                page = "volunteer_updated.html"
            v.requested = vf.cleaned_data['requested']
            v.comments = vf.cleaned_data['comments']
            v.volunteer = profile
            v.save()
            # should send an email at this point
            return render_to_response(page,
                                      context_instance=RequestContext(request))

    else:
        vf = VolunteerForm(instance=instance)

    return render_to_response("call_for_volunteers.html",
                              { "volunteers_form" : vf },
                              context_instance=RequestContext(request))

@permission_required("volunteers.change_volunteer")
def manage(request, vol_id):
    volunteer = get_object_or_404(Volunteer, id=vol_id)

    if request.method == 'POST':
        vf = VolunteerForm(request.POST, instance=volunteer)
        if vf.is_valid():
            vf.save()
            return HttpResponseRedirect("/volunteer/list/")
#            return render_to_response("volunteer_list.html",
#                                      {"volunteers_form" : vf, 
#                                       "volunteer": volunteer },
#                                      context_instance=RequestContext(request))
    else:
        vf = VolunteerForm(instance=volunteer)

    return render_to_response("volunteer_manage.html",
                              { "volunteers_form": vf, "volunteer": volunteer },
                              context_instance=RequestContext(request))

@permission_required("volunteers.change_volunteer")
def list(request):
    volunteer_list = Volunteer.objects.all()
    return render_to_response("volunteer_list.html",
                              { "volunteer_list" : volunteer_list },
                              context_instance=RequestContext(request))

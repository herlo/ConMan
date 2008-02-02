# Create your views here.
from django.http import HttpResponseRedirect, Http404, HttpRequest, HttpResponse
from django.core.urlresolvers import reverse 
from django.shortcuts import render_to_response
from common.models import Volunteer, UserProfile, VolunteerRole, ShirtSize
from common.forms import VolunteerForm
from common.config import Static
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login


def index(request):
    isinstance(request,HttpRequest)

    vf = VolunteerForm()
    if request.method == 'POST':
        vf = VolunteerForm(request.POST)
        if not vf.is_valid():
            return render_to_response('call_for_volunteers.html',{'volunteer_form':vf})
        else:
            user = save_user(request, vf)
            profile = save_user_profile(request, user, "volunteer")
            try:
                user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            except AuthenticationError e:
                return render_to_response('login.html', {'error': e})
            return render_to_response('volunteer_submitted.html', {'user': profile})
    else:
        print request.method
        return render_to_response('call_for_volunteers.html', {'volunteers_form': vf} )

def submitted(request, v_id):
    v = get_object_or_404(Volunteer, pk=v_id)
    u = User.objects.get(id=v_id)
    m = Static.vol_email_msg
    v.email_user(con_form.data['subject'], m, u.email)
    return render_to_response('volunteer_submitted.html', {'user': v.user})


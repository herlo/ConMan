# Create your views here.
from django.http import HttpResponseRedirect, Http404, HttpRequest, HttpResponse
from django.core.urlresolvers import reverse 
from django.shortcuts import render_to_response
from common.models import Volunteer, UserProfile, VolunteerRole, ShirtSize
from common.forms import VolunteerForm
from common.views import *
from common.config import Static
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login

def index(request):
    isinstance(request,HttpRequest)

    vf = VolunteerForm()
    if request.method == 'POST':
        vf = VolunteerForm(request.POST)
        if not vf.is_valid():
            return render_to_response('call_for_volunteers.html', {'volunteer_form':vf})
        else:
            user = save_user(request, vf)
            profile = save_user_profile(request, user, vf, "volunteer")
            try:
                user = authenticate(username=vf.cleaned_data['username'],password=vf.cleaned_data['password'])
            except e:
                return render_to_response('login.html', {'error': e})

            userinfo = dict()
            userinfo['name']= user.get_full_name()
            userinfo['email']= user.email
            return render_to_response('volunteer_submitted.html', {'user': userinfo})
    else:
        if request.user.is_authenticated():
            isinstance(vf.fields,dict)
            vf.fields.pop('username')
            vf.fields.pop('password')
            vf.fields.pop('confirm_password')

        print request.method
        return render_to_response('call_for_volunteers.html', {'volunteers_form': vf} )

def submitted(request, v_id):
    v = get_object_or_404(Volunteer, pk=v_id)
    u = User.objects.get(id=v_id)
    m = Static.VOL_EMAIL_MSG
    v.email_user(con_form.data['subject'], m, u.email)
    return render_to_response('volunteer_submitted.html', {'user': v.user})


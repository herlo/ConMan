# Create your views here.
from django.http import HttpResponseRedirect, Http404, HttpRequest, HttpResponse
from django.core.urlresolvers import reverse 
from django.shortcuts import render_to_response
from common.models import Volunteer, UserProfile, VolunteerRole, ShirtSize
from common.forms import VolunteerForm
from django.contrib.auth.models import User,UserManager
from django.contrib.auth import authenticate,login

def index(request):
    isinstance(request,HttpRequest)

    vf = VolunteerForm()
    if request.method == 'POST':
        vf = VolunteerForm(request.POST)
        if not vf.is_valid():
            return render_to_response('call_for_volunteers.html',{'volunteer_form':vf})
        else:
            if request.user.is_anonymous():
                user = User.objects.create_user(vf.cleaned_data['username'], vf.cleaned_data['email'], password = vf.cleaned_data['password'])
                isinstance(user, User)
            else:
                user = authenticate(username=request.user.username,password=request.user.password) 
            print request.user.is_anonymous()
            user.first_name = vf.cleaned_data['first_name']
            user.last_name = vf.cleaned_data['last_name']
            user.save()
            profile = None
    
            try:
                profile = user.get_profile()
            except :
                print 'No Profile Found'
    
            r = VolunteerRole.objects.get(id=vf.cleaned_data['requested_role'])
            profile = UserProfile.objects.create(user=user,
                    bio = '', 
                    shirtsize=ShirtSize.objects.get(id=vf.cleaned_data['shirt_size']),
                    job_title=vf.cleaned_data['job_title'],
                    irc_nick=vf.cleaned_data['irc_nick'], 
                    irc_server=vf.cleaned_data['irc_server'],
                    common_channels=vf.cleaned_data['irc_channels'])
    
            user2 =authenticate(username=vf.cleaned_data['username'],password=vf.cleaned_data['password'])
            userinfo = dict()
            userinfo['name']= user2.get_full_name()
            userinfo['email']= user2.email

	    print "userinfo: " + str(profile) 
    
            return render_to_response('volunteer_submitted.html', {'user': userinfo})
    else:
        print request.method
        return render_to_response('call_for_volunteers.html', {'volunteers_form': vf} )

def submitted(request, v_id):
    v = get_object_or_404(Volunteer, pk=v_id)
    return render_to_response('volunteer_submitted.html', {'user': v.user})

## Create your views here.
#from django.contrib.auth.models import User,UserManager,Group
#from django.http import HttpResponseRedirect, Http404, HttpRequest, HttpResponse
#from django.contrib.auth import authenticate,login
#from django.shortcuts import render_to_response
#from django.core.urlresolvers import reverse 

#from common.models import ShirtSize, UserProfile
#from common.config import Static

#from volunteers.models import Volunteer, VolunteerRole
#from volunteers.forms import VolunteerForm

#def index(request):
    #isinstance(request,HttpRequest)

    #vf = VolunteerForm()
    #if request.method == 'POST':
        #vf = VolunteerForm(request.POST)
        #if not vf.is_valid():
            #return render_to_response('call_for_volunteers.html', {'volunteer_form':vf})
        #else:
            #user = save_user(request, vf)
            #profile = save_user_profile(request, user, vf, "volunteer")
            #try:
                #user = authenticate(username=vf.cleaned_data['username'],password=vf.cleaned_data['password'])
            #except e:
                #return render_to_response('login.html', {'error': e})

            #userinfo = dict()
            #userinfo['name']= user.get_full_name()
            #userinfo['email']= user.email
            #return render_to_response('volunteer_submitted.html', {'user': userinfo})
    #else:
        ##if request.user.is_authenticated():
            ##isinstance(vf.fields,dict)
            ##vf.fields.pop('username')
            ##vf.fields.pop('password')
            ##vf.fields.pop('confirm_password')

        #print request.method
        #return render_to_response('call_for_volunteers.html', {'volunteers_form': vf} )

#def save_volunteer(request, form):
    #role = VolunteerRole.objects.get(id=form.cleaned_data['requested_role'])
    #UserProfile.objects.create(request=role, comments=form.cleaned_data['comments'])    

#def submitted(request, v_id):
    #v = get_object_or_404(Volunteer, pk=v_id)
    #u = User.objects.get(id=v_id)
    #m = Static.VOL_EMAIL_MSG
    #v.email_user(con_form.data['subject'], m, u.email)
    #return render_to_response('volunteer_submitted.html', {'user': v.user})


# Create your views here.
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django import newforms as forms
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.mail import *
from django.conf import settings

from cStringIO import StringIO
import pdb,random
import Image,ImageDraw,ImageFont

from common.models import ShirtSize
from speakers.models import Category,Status
from speakers.forms import *


def send_confirm_email(user, form):
    #send the email here (note we could probably do this in one place later on)
    current_site = settings.HOST_NAME
    
    p = dict()
#    p['cat'] = mark_safe(str(Category.objects.get(id=form.cleaned_data['category'])))
    p['role'] = mark_safe(form.cleaned_data['role'])
#    p['audience'] = mark_safe(str(AudienceType.objects.get(id=form.cleaned_data['audience'])))
    p['comment'] = mark_safe(form.cleaned_data['comment'])
    p['name'] = mark_safe(user.first_name + ' ' + user.last_name)
    
    subject = render_to_string('volunteer_confirm_subject.txt')
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    
    message = render_to_string('volunteer_confirm.txt',
                               { 'vol': v })
    
    if settings.SEND_EMAIL:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        mail_managers(subject, message, fail_silently=True)
    else:
        print "Subject: " + subject
        print "Message: " + message
        print "Sent to: " + user.email

@login_required
def index(request, vol_id=None):
    isinstance(request,HttpRequest)
    user = User.objects.get(id=request.session.get('_auth_user_id'))
    print "User is: " + str(user)
    userinfo = dict()
    userinfo['name']= user.get_full_name()
    userinfo['email']= user.email

    volunteer_exists = False

    if vol_id:
        instance = get_object_or_404(Volunteer, id=vol_id)
        volunteer_exists = True
    else:
        instance = Volunteer(volunteer=request.user.get_profile())

    if request.method == 'POST':
        vf = VolunteerForm(request.POST, instance=instance)
        if not vf.is_valid():
            return render_to_response('call_for_volunteers.html',{'volunteer_form':vf},
                context_instance=RequestContext(request))
        else:
            vf.save()
            send_confirm_email(user, vf)
            if volunteer_exists:
                return render_to_response('volunteer_updated.html', {'host': settings.HOST_NAME}, context_instance=RequestContext(request))
            else:
                return render_to_response('volunteer_submitted.html', {'host': settings.HOST_NAME}, context_instance=RequestContext(request))
    else:
        vf = VolunteerForm(instance=instance)
        #abstracts = Volunteer.objects.filter(volunteer=user.get_profile())
        return render_to_response('call_for_volunteers.html',{'volunteer_form':vf}, context_instance=RequestContext(request))

@login_required
def delete_abstract(request, abs_id=None):
    pass

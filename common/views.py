# Create your views here.
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
from common.models import User,UserProfile
from common.forms import *
from common.config import Static
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

#def save_user(request, form):
#    print "in save_user beginning"
#    if request.user.is_anonymous():
#        try:
#            luser = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
#        except:
#            return render_to_response('accounts/login.html', {'error': Static.USER_ALREADY_EXISTS})
#    else:
#        luser = User(request.user)
#
#    print "Luser info: " + str(luser.username)
#
#    luser.first_name = form.cleaned_data['first_name']
#    luser.last_name = form.cleaned_data['last_name']
##    luser.groups.add(Group.objects.get(id=5))
#    luser.save()
#    #pdb.set_trace()
#    return luser

#from settings import SEND_EMAIL
#
#def send_email(user, email):
#    if SEND_EMAIL:
#        user.email_user(email['subject'],email['txt'],user.email)
#    else:
#        print "sent email"

def show_tos(request):
    return render_to_response('tos.html')

def mass_email(request, users):
    if request.method == 'POST':
        for selected in request.POST.getlist('users'):
            # send email here
            user = User.objects.get(pk=selected)
            user.email_user(request.POST['subject'],
                request.POST['email'], settings.DEFAULT_FROM_EMAIL) 

    return render_to_response('mass_email.html', {'users': users}, context_instance=RequestContext(request))

def test(request):
    volunteer_form = VolunteerForm()
    presenter_form = SpeakerForm()
    if request.method == 'POST':
        presenter_form = SpeakerForm(request.POST)
    if not presenter_form.is_valid():
        return render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})
    return render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})

def index(request):
    return HttpResponseRedirect('/pages/home/')

def contact(request):
    con_form = ContactUsForm()
    if request.method == 'POST':
        con_form = ContactUsForm(request.POST)
        if con_form.is_valid:
            admin = User.objects.filter(is_superuser__exact=True)
            for u in admin:
                u.email_user(con_form.data['subject'],con_form.data['message'],'conference@utos.org')
            print u.username

            return HttpResponseRedirect('/')
    else:
#        captcha = generate_sum_captcha()
        con_form.data = {'captcha_uid':captcha.uid}
        return render_to_response('contactus.html',{'contactform':con_form})


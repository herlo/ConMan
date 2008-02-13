# Create your views here.
from django.shortcuts import render_to_response
from common.models import *
from common.forms import *
from common.views import *
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.utils.datastructures import SortedDict
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login
import pdb

#def save_speaker(request, form):
#    #user = save_user(request, form)
#    if request.user.is_anonymous():
#        try:
#            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
#        except:
#            return render_to_response('call_for_papers.html', {'error': 'Username ' + form.cleaned_data['username'] + ' already chosen, please try again'})
#        
#        print "created user"
#        if (isinstance(user, User)):
#            print "this is an instance? "
#        else:
#            return render_to_response('registration/login.html', {'error': Static.USER_ALREADY_EXISTS})
#    else:
#        user = User(request.user)
#
#    user.first_name = form.cleaned_data['first_name']
#    user.last_name = form.cleaned_data['last_name']
#    user.groups.add(Group.objects.get(name__exact='Speaker'))
#    user.save()
#    print "FullName: " + user.get_full_name()
#    #pdb.set_trace()
#    pres = Presentation.objects.create(
#        cat = Category(form.cleaned_data['category']),
#        audience = AudienceType(form.cleaned_data['audience']),
#        short_abstract = form.cleaned_data['short_abstract'],
#        #long_abstract = form.cleaned_data['longabstract'],
#        status = 'Pending',
#        title = form.cleaned_data['title'],
##        slides = form.clean_data(upload_to="slides",blank=True,null=True) 
#    )
#    pres.save()
#
#    up = UserProfile.objects.create(user=user,
#      bio = form.cleaned_data['bio'],
#      presentation=pres,
#      shirtsize=ShirtSize.objects.get(id=form.cleaned_data['shirt_size']),
#      job_title=form.cleaned_data['job_title'],
#      irc_nick=form.cleaned_data['irc_nick'],
#      irc_server=form.cleaned_data['irc_server'],
#      common_channels=form.cleaned_data['irc_channels'])
#    up.save()
#
#    #user = authenticate(username=pf.cleaned_data['username'],password=pf.cleaned_data['password'])
#
##    pdb.set_trace()
#    usrinfo = dict()
#    usrinfo['name']= user.get_full_name()
#    usrinfo['email']= user.email
#    pw = request.POST['password']
#
#    email = dict()
#    email['subject'] = Static.ABSTR_EMAIL_SUBJECT
#    email['txt'] = 'Name: ' + userinfo['name'] + '\nUsername: ' + user.username + '\nPassword: ' + pw + '\n\n' + Static.ABSTR_EMAIL_CONFIRM
#    send_email(user, email)
#    return user

def index(request):
    isinstance(request,HttpRequest)
#    pdb.set_trace()
    user = User()
    pf = SpeakerForm()
    if request.method == 'POST':
        pf = SpeakerForm(request.POST)
        #print request.POST
        if not pf.is_valid():
            #captcha = generate_sum_captcha()
            #pf.data = {'captcha_uid':captcha.uid}
            return render_to_response('call_for_papers.html',{'presenter_form':pf})
        else:
            #CaptchaRequest.validate(pf.data['captcha_uid'],pf.data['captcha_text'])
            #user = save_speaker(request, pf)
            if request.user.is_anonymous():
                user = User.objects.create_user(pf.cleaned_data['username'], pf.cleaned_data['email'], pf.cleaned_data['password'])
                user.save()
                if not isinstance(user, User):
                    return render_to_response('call_for_papers.html', {'presenter_form':pf,'error': Static.USER_ALREADY_EXISTS})
            else:
                user = User(request.user)
        
            user.first_name = pf.cleaned_data['first_name']
            user.last_name = pf.cleaned_data['last_name']
            user.groups.add(Group.objects.get(name__exact='Speaker'))
            user.save()
            print "saved user"
            print user.get_full_name()
            #pdb.set_trace()
            pres = Presentation.objects.create(
                cat = Category(pf.cleaned_data['category']),
                audience = AudienceType(pf.cleaned_data['audience']),
                short_abstract = pf.cleaned_data['short_abstract'],
                #long_abstract = pf.cleaned_data['longabstract'],
                status = 'Pending',
                title = pf.cleaned_data['title'],
        #        slides = pf.clean_data(upload_to="slides",blank=True,null=True) 
            )
            pres.save()
            print "saved presentation"
        
            up = UserProfile.objects.create(user=user,
              bio = pf.cleaned_data['bio'],
              presentation=pres,
              shirtsize=ShirtSize.objects.get(id=pf.cleaned_data['shirt_size']),
              job_title=pf.cleaned_data['job_title'],
              irc_nick=pf.cleaned_data['irc_nick'],
              irc_server=pf.cleaned_data['irc_server'],
              common_channels=pf.cleaned_data['irc_channels'])
            up.save()
        
            #user.groups.add(Group.objects.get(id=4))
            #user = authenticate(username=pf.cleaned_data['username'],password=pf.cleaned_data['password'])
            #login(request, user)

        #    pdb.set_trace()
            usrinfo = dict()
            usrinfo['name']= user.get_full_name()
            usrinfo['email']= user.email
            pw = request.POST['password']
        
            email = dict()
            email['subject'] = Static.ABSTR_EMAIL_SUBJECT
            email['txt'] = usrinfo['name'] + '\nUsername: ' + user.username + '\nPassword: ' + pw + '\n\n' + Static.ABSTR_EMAIL_CONFIRM
            send_email(user, email)

            return render_to_response('paper_submitted.html',{'user':user})
    else:
        if request.user.is_authenticated():
            isinstance(pf.fields, SortedDict)
            #pf.fields.pop('username')
            #pf.fields.pop('password')
            #pf.fields.pop('confirm_password')
        return render_to_response('call_for_papers.html',{'presenter_form':pf})


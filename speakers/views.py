# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.mail import *
#from django.utils.safestring import mark_safe

from cStringIO import StringIO
import pdb,random
import Image,ImageDraw,ImageFont

from common.models import ShirtSize
from speakers.forms import *

def save_presentation(request, form, user):

    pres = Presentation.objects.create(
        presenter=user,
        cat = Category(form.cleaned_data['category']),
#        audience = audience
        short_abstract = form.cleaned_data['short_abstract'],
        #long_abstract = form.cleaned_data['longabstract'],
        status = 'Pending',
        title = form.cleaned_data['title'],
#        slides = form.cleaned_data(upload_to="slides",blank=True,null=True) 
    )

    print "audiences: " 
    auds = form.cleaned_data['audience']
    for aud in auds:
        print aud
        pres.audiences.add(aud)

    pres.save()
    

    user.groups.add(Group.objects.get(id=5))
    up = user.get_profile()

    #print "up: " + str(up)
    up.presentation_set.add(pres)
    up.save()

    #send the email here (note we could probably do this in one place later on)
    current_site = settings.HOST_NAME
    
    p = dict()
#    p['cat'] = mark_safe(str(Category.objects.get(id=form.cleaned_data['category'])))
    p['title'] = mark_safe(form.cleaned_data['title'])
#    p['audience'] = mark_safe(str(AudienceType.objects.get(id=form.cleaned_data['audience'])))
    p['abstract'] = mark_safe(form.cleaned_data['short_abstract'])
    p['name'] = mark_safe(user.first_name + ' ' + user.last_name)
    
    subject = render_to_string('presentation_confirm_subject.txt')
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    
    message = render_to_string('presentation_confirm.txt',
                               { 'pres': p })
    
    if settings.SEND_EMAIL:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        mail_managers(subject, message, fail_silently=True)
    else:
        print "Subject: " + subject
        print "Message: " + message
        print "Sent to: " + user.email

#        return render_to_response('error.html', {'error': Static.USER_ALREADY_EXISTS})

@login_required
def index(request):
    isinstance(request,HttpRequest)
    #save_user_profile(request, user, pf, "speaker")
    user = User.objects.get(id=request.session.get('_auth_user_id'))
#    print "User is: " + str(user)
    userinfo = dict()
    userinfo['name']= user.get_full_name()
    userinfo['email']= user.email

    pf = SpeakerForm()
    if request.method == 'POST':
        pf = SpeakerForm(request.POST)
#        print request.POST
        if not pf.is_valid():
            print "pf isn't valid"
#            captcha = generate_sum_captcha()
#            return render_to_response('call_for_papers.html',{'presenter_form':pf, 'captcha_uid':captcha.uid, 'captcha_text':captcha.text})
            return render_to_response('call_for_papers.html',{'presenter_form':pf},
                context_instance=RequestContext(request))
        else:
#            is_valid_captcha = CaptchaRequest.validate(pf.data['captcha_uid'],pf.data['captcha_text'])
#            if is_valid_captcha != 1:
#                captcha = generate_sum_captcha()
#                return render_to_response('call_for_papers.html',{'presenter_form':pf})
#                return render_to_response('call_for_papers.html',{'presenter_form':pf, 'captcha_uid':captcha.uid, 'captcha_text':captcha.text})

#            pdb.set_trace()
            print "session: " 
            print request.session.items()
            save_presentation(request, pf, user)

            return render_to_response('paper_submitted.html', {'user': user},
                context_instance=RequestContext(request))
    else:
        return render_to_response('call_for_papers.html',{'presenter_form':pf},
            context_instance=RequestContext(request))

        #captcha = generate_sum_captcha()
#        return render_to_response('call_for_papers.html',{'presenter_form':pf, 'captcha_uid':captcha.uid, 'captcha_text':captcha.text, 'user': userinfo})

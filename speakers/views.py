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
from django.core.urlresolvers import reverse


from cStringIO import StringIO
import pdb,random
import Image,ImageDraw,ImageFont

import settings
from common.models import ShirtSize
from speakers.models import Category,Status
from speakers.forms import *


def send_confirm_email(user, form):
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

@login_required
def abstract(request, abs_id=None):
    isinstance(request,HttpRequest)
    user = User.objects.get(id=request.session.get('_auth_user_id'))
    print "User is: " + str(user)
    userinfo = dict()
    userinfo['name']= user.get_full_name()
    userinfo['email']= user.email

    presentation_exists = False

    if abs_id:
        instance = get_object_or_404(Presentation, id=abs_id)
        presentation_exists = True
    else:
        instance = Presentation(presenter=request.user.get_profile())

    if request.method == 'POST':
        pf = PresentationForm(request.POST, instance=instance)
        if not pf.is_valid():
            return render_to_response('call_for_papers.html',{'presenter_form':pf},
                context_instance=RequestContext(request))
        else:
            pf.save()
            send_confirm_email(user, pf)
            if presentation_exists:
                return render_to_response('paper_updated.html', {'host': settings.HOST_NAME}, context_instance=RequestContext(request))
            else:
                return render_to_response('paper_submitted.html', {'host': settings.HOST_NAME}, context_instance=RequestContext(request))
    else:
        pf = PresentationForm(instance=instance)
        abstracts = Presentation.objects.filter(presenter=user.get_profile())
        return render_to_response('call_for_papers.html',{'presenter_form':pf,
        'abstract_list':abstracts, 'abs_id': abs_id, 'presentation_exists': presentation_exists}, context_instance=RequestContext(request))

@login_required
def delete_abstract(request, abs_id):
    instance = get_object_or_404(Presentation, id=abs_id)
    instance.delete()
    pf = PresentationForm()
    deletedText = settings.PRESENTATION_DELETED
    return render_to_response('call_for_papers.html', {'presenter_form': pf, 'deleted': deletedText }, context_instance=RequestContext(request))

def show_speakers(request):
    pass




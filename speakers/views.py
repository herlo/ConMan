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
#    print "User is: " + str(user)
    userinfo = dict()
    userinfo['name']= user.get_full_name()
    userinfo['email']= user.email

    presentation_exists = False

    print "Abs id: " + str(abs_id)

    if abs_id:
        instance = get_object_or_404(Presentation, id=abs_id)
        presentation_exists = True
    else:
        group = Group.objects.get(name='Speaker')
        user.groups.add(group)
        user.save()
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
        abstracts = Presentation.objects.filter(presenter=user.get_profile()).exclude(status__name='Approved')
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
    group = Group.objects.get(name='Speaker')
    speakers = group.user_set.all().order_by('last_name')
    try:
        user = User.objects.get(id=request.session.get('_auth_user_id'))
    except:
        user = None
        
    speaker_list = list()

    for speaker in speakers:
        presentations = list()
        profile = speaker.get_profile()
        if isinstance(user,User) and user.has_perm('can_vote'):
            pending_list = profile.presentation_set.filter(status=Status.objects.get(name='Pending'))
        approved_list = profile.presentation_set.filter(status=Status.objects.get(name='Approved'))

        if (len(approved_list)):
            for p in approved_list:
                presentations.append({'id': p.id, 'title': p.title, 'status': p.status})
        if (len(pending_list)):
            for p in pending_list:
                presentations.append({'id': p.id, 'title': p.title, 'status': p.status})
    
            speaker_list.append({ 'id': speaker.id, 'name': speaker.get_full_name(), 'company': profile.company, 'bio': profile.bio, 'irc_nick': profile.irc_nick, 'irc_server':
            profile.irc_server, 'job_title': profile.job_title, 'web_site':
            profile.site, 'photo': profile.user_photo, 'presentations': presentations})


    return render_to_response('show_speakers.html', {'speakers': speaker_list
    }, context_instance=RequestContext(request))

def show_presentation(request, p_id):
    p = get_object_or_404(Presentation, id=p_id)
    presentation = dict()

    spkr = p.presenter
    spkr_id = spkr.user.id
#    print "spkr id: " +str(spkr.id)
    spkr_name = spkr.user.get_full_name()

    return render_to_response('show_presentation.html', {'presentation':
    p, 'spkr': spkr, 'spkr_name': spkr_name, 'spkr_id': spkr_id},
    context_instance=RequestContext(request))

def speaker_info(request, s_id):
    status = Status.objects.get(name='Approved')
    spkr = get_object_or_404(User, id=s_id)

    profile = spkr.get_profile()
    pres_list = profile.presentation_set.filter(status=status)

    return render_to_response('show_speaker.html', {'spkr': spkr, 'profile':
    profile, 'presentations': pres_list})


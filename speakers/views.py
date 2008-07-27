# Create your views here.
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django import newforms as forms
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from datetime import datetime
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.mail import *
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test

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

# helper method for uploading files
def handle_uploaded_file(file, path):
    filename = path
    print "Filename: " + filename
    destination = open(filename, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)

@login_required
def abstract(request, abs_id=None):
    # Get or create the Presentation instance for the forms
    isinstance(request,HttpRequest)
    user = User.objects.get(id=request.session.get('_auth_user_id'))

    approved_status = Status.objects.get(name='Approved')
    presentation_exists = False

    if abs_id:
        instance = get_object_or_404(Presentation, id=abs_id, presenter=user.get_profile())
    else:
        group = Group.objects.get(name='Speaker')
        user.groups.add(group)
        user.save()
        instance = Presentation(presenter=request.user.get_profile())

    if request.method == 'POST':
        if instance.status.name != 'Approved':
            pf = PresentationForm(request.POST, request.FILES, instance=instance)
            if pf.is_valid():
#                handle_uploaded_file(request.FILES['slides'])
                pf.save()
                send_confirm_email(user, pf)

                if abs_id:
                    return render_to_response('paper_updated.html',
                        {'host': settings.HOST_NAME},
                        context_instance=RequestContext(request))
                else:
                    return render_to_response('paper_submitted.html',
                        {'host': settings.HOST_NAME},
                        context_instance=RequestContext(request))
        else: # Presentation is approved
            sf = PresentationSlidesForm(request.POST, request.FILES, instance=instance)
            if sf.is_valid():
                print "Filename sent: " + instance.get_slides_filename()
                handle_uploaded_file(request.FILES['slides'], instance.get_slides_filename())
                sf.save()
                return render_to_response('paper_updated.html',
                    {'host': settings.HOST_NAME},
                    context_instance=RequestContext(request))

    else: # GET
        pf = PresentationForm(instance=instance)
        sf = PresentationSlidesForm(instance=instance)
        abstracts = Presentation.objects.filter(presenter=user.get_profile())

    return render_to_response('call_for_papers.html', {
                'presenter_form': pf,
                'slides_form': sf,
                'abstract_list':abstracts,
                'abs_id': abs_id,
                'approved_status': approved_status,
                'presentation_exists': bool(abs_id)
            }, context_instance=RequestContext(request))

@login_required
def delete_abstract(request, abs_id):
    instance = get_object_or_404(Presentation, id=abs_id)
    instance.delete()
    pf = PresentationForm()
    deletedText = settings.PRESENTATION_DELETED
    return render_to_response('call_for_papers.html', {'presenter_form': pf, 'deleted': deletedText }, context_instance=RequestContext(request))
    
def show_presentation_schedule(request, day="1970-01-01"):
#    print "Day: " + day
    date = datetime(1970, 01, 01)
    if day:
        d = day.rsplit("-")
    #    print "Date: " + str(d)
        date = datetime(int(d[0]), int(d[1]), int(d[2]))
        presentations = Presentation.objects.filter(status=Status.objects.get(name='Approved')).filter(start__month=date.month).filter(start__day=date.day).order_by('start')
        template = 'show_presentation_day.html'
    else:
        presentations = Presentation.objects.filter(status=Status.objects.get(name='Approved')).order_by('start')
        #print "Presentation: " + p.title + " " + str(p.start)
        template = 'show_presentations.html'
        
    return render_to_response(template, {'day': date, 'presentations': presentations }, context_instance=RequestContext(request))

def show_speakers(request):
    #print "in show_speakers"
    group = Group.objects.get(name='Speaker')
    speakers = group.user_set.all().order_by('last_name')

    user = request.user

    speaker_list = list()
    pending_list = list()

    for speaker in speakers:
        presentations = list()
        profile = speaker.get_profile()
        
        if isinstance(user,User) and (user.has_perm('voting.add_vote') or
            user.has_perm('voting.change_vote') or
            user.has_perm('voting.delete_vote')):
            pending_list = profile.presentation_set.filter(status=Status.objects.get(name='Pending'))
            for p in pending_list:
                presentations.append({'id': p.id, 'title': p.title, 'status': p.status})

        approved_list = profile.presentation_set.filter(status=Status.objects.get(name='Approved')).order_by('start')

        if (len(approved_list)):
            for p in approved_list:
                presentations.append({'id': p.id, 'title': p.title, 'status': p.status, 'start': p.start})
                print "Presentation: " + p.title + " " + str(p.start)

        if (presentations):
            speaker_list.append({ 'id': speaker.id, 'name': speaker.get_full_name(), 'company': profile.company, 'bio': profile.bio, 'irc_nick': profile.irc_nick, 'irc_server':
            profile.irc_server, 'job_title': profile.job_title, 'web_site':
            profile.site, 'photo': profile.user_photo, 'presentations': presentations})


    return render_to_response('show_speakers.html', {'speakers': speaker_list }, context_instance=RequestContext(request))


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
    profile, 'presentations': pres_list}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def voting_results(request):
    """Report on the django-voting results for all presentations."""
    return render_to_response(
            'admin/speakers/presentation/voting_results.html',
            {'object_list': Presentation.objects.all()},
            context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def show_speakers_admin(request):
    """Display a list of users who are in the speakers group"""

    users = User.objects.all()

#    perms = users.get_all_permissions()
#
#    print "Perms: " + str(perms)
    speakers = list()

    for user in users:
        if user.has_perm('speakers.add_presentation'):
            speakers.append(user)

            if request.method == 'POST':
    
                if settings.SEND_EMAIL:
                    # send email here
                    speakers.email_user(request.POST['subject'],
                        request.POST['email'], settings.DEFAULT_FROM_EMAIL) 
                else:
                    print "To: " + user.first_name + "\nFrom: " + settings.DEFAULT_FROM_EMAIL + "\nSubject: " + request.POST['subject'] + "\nEmail: " + request.POST['email'] + "\n\nCheers,\n\nClint Savage\n\nhttp://utosc.com \| http://utos.org"


    return render_to_response(
            'admin/speakers/show_speakers.html', 
            {'object_list': speakers, 'description': "Speaker Name"  },
            context_instance=RequestContext(request))
















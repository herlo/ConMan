# Create your views here.
from django import forms as forms
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.utils import simplejson
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
from django.db.models import Q

from cStringIO import StringIO
from datetime import datetime
import pdb,random
import Image,ImageDraw,ImageFont

import settings
from common.models import ShirtSize
from speakers.models import Category,Status,Presentation,AudienceType
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
    
    filename = settings.MEDIA_ROOT + str(file.name)
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
        instance = get_object_or_404(Presentation, id=abs_id)
        page_to_render = 'update_abstract.html'
    else:
        page_to_render = 'call_for_papers.html'
        instance = Presentation()

    group = Group.objects.get(name='Speaker')

    if request.method == 'POST':
        if instance.status.name != 'Approved':
            # get the list of presenters
            users = request.POST.getlist('presenter')
            print "1 users: " + str(users)

            #
            # validate that the required fields have values
            #
            if request.POST['title'] != None and request.POST['short_abstract'] != None and request.POST['cat'] != None and request.POST.has_key('audiences') and request.POST['audiences'] != None:
                instance.save()

            instance.save()
            for u in users:
                if u:
                    user = User.objects.get(id=u)
                    print "user: " + str(user)
                    user.groups.add(group)
                    user.save()
                    p=user.get_profile()
                    instance.presenter.add(p)
            instance.save()

            pf = PresentationForm(request.POST, request.FILES, instance=instance)
            sf = PresentationSlidesForm(instance=instance)
            abstracts = None
            if pf.is_valid():
                prfrm = pf.save(commit=False)
                print "2 users: " + str(users)
                for u in users:
                    user = User.objects.get(id=u)
                    print "3 user: " + str(user)
                    prfrm.presenter.add(user.get_profile())
                    prfrm.save()
                    send_confirm_email(user, pf)
                pf.save_m2m()
                pf.save()

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
                handle_uploaded_file(request.FILES['slides'], user.username)
                sf.save()
                return render_to_response('paper_updated.html',
                    {'host': settings.HOST_NAME},
                    context_instance=RequestContext(request))

    else: # GET
        pf = PresentationForm(instance=instance)
        sf = PresentationSlidesForm(instance=instance)
        abstracts = Presentation.objects.filter(presenter=user.get_profile())
        if abs_id:
            presentation = Presentation.objects.get(id=abs_id)
        else:
            presentation = Presentation()

    return render_to_response(page_to_render, {
                'presentation': presentation,
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
    
def show_presentation_schedule(request, day=None, cat=None, room=None, audience=None):
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
        template = 'show_presentations.html'
        
    return render_to_response(template, {'day': date, 'presentations': presentations }, context_instance=RequestContext(request))

def show_speakers(request, status='all'):
    group = Group.objects.get(name='Speaker')
    speakers = group.user_set.all().order_by('last_name')

    user = request.user
    feed = False

    speaker_list = list()

    for speaker in speakers:
        presentations = list()
        profile = speaker.get_profile()
        
        if (status == 'all'):
            pending_list = profile.presentation_set.filter(status=Status.objects.get(name='Pending'))
            approved_list = None
            feed = True
        else:
            if isinstance(user,User) and (user.has_perm('voting.add_vote') 
                    or user.has_perm('voting.change_vote') or user.has_perm('voting.delete_vote')):
                pending_list = profile.presentation_set.filter(status=Status.objects.get(name='Pending'))

            approved_list = profile.presentation_set.filter(status=Status.objects.get(name='Approved')).order_by('start')
    
            if (len(approved_list)):
                for p in approved_list:
                    presentations.append({'id': p.id, 'title': p.title, 'status': p.status, 'start': p.start})

        for p in pending_list:
            presentations.append({'id': p.id, 'title': p.title, 'status': p.status})

        if (presentations):
            speaker_list.append({ 'id': speaker.id, 'name': speaker.get_full_name(), 'company': profile.company, 'bio': profile.bio, 'irc_nick': profile.irc_nick, 'irc_server': profile.irc_server, 'job_title': profile.job_title, 'web_site': profile.site, 'photo': profile.user_photo, 'presentations': presentations})

    #keep this indented here, don't move it unless you want things to not work!
    return render_to_response('show_speakers.html', {'speakers': speaker_list, 'feed': feed}, context_instance=RequestContext(request))

def show_presentations(request):
    # grab the presentions
    presentations = Presentation.objects.all().order_by('cat')

    return render_to_response('show_presentations.html', {'presentations': presentations}, context_instance=RequestContext(request))
    
def show_presentation(request, p_id):
    p = get_object_or_404(Presentation, id=p_id)

    speakers = p.presenter.all()
    spkr_list = list()
    count = 0
    multiple = False
    for s in speakers:
        spkr_id = s.user.id
        spkr_name = s.user.get_full_name()
        spkr_list.append({'spkr': s, 'name': spkr_name, 'id': spkr_id})
        count = count + 1

    if count > 1:
        multiple = True

    return render_to_response('show_presentation.html', { 'presentation': p, 'spkr': spkr_list, 'multiple': multiple },
    context_instance=RequestContext(request))

def speaker_info(request, s_id):
    status = Status.objects.get(name='Approved')
    spkr = get_object_or_404(User, id=s_id)

    profile = spkr.get_profile()
    pres_list = profile.presentation_set.filter(status=status)

    return render_to_response('show_speaker.html', {'spkr': spkr, 'profile':
    profile, 'presentations': pres_list}, context_instance=RequestContext(request))

def find_speakers(request, search=None):
 #    if request.method == 'POST':
        if search:
            user_list = User.objects.filter(Q(username__contains=search) | Q(first_name__contains=search) | Q(last_name__contains=search))
    
            users = list()
            for user in user_list:
                profile = user.get_profile()
                users.append({ 'id': user.id, 'name': user.get_full_name(), 
                    'company': profile.company,  'job_title': profile.job_title})
    
            json = simplejson.dumps(users)
            return HttpResponse(json, mimetype='application/json')
    #        return render_to_response('find_speakers.html', {'speakers': user_list }, context_instance=RequestContext(request))
        else:
            pass
                #show the search form with errors
#    else:
#        return render_to_response('find_speakers.html', context_instance=RequestContext(request))


def list_audiences(request):
    items = AudienceType.objects.all()
    page_info = { 'title': 'Audiences', 'item_name_heading': 'Audience Type', 'item_value_heading': 'Description' }

    return render_to_response('generic_list.html', {'items': items, 'page_info': page_info }, context_instance=RequestContext(request))

def list_categories(request):
    items = Category.objects.all()
    page_info = { 'title': 'Categories', 'item_name_heading': 'Category Name', 'item_value_heading': 'Description' }

    return render_to_response('generic_list.html', {'items': items, 'page_info': page_info }, context_instance=RequestContext(request))

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

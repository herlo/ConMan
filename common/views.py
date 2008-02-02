# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from common.models import User,UserProfile,Presentation,Category,PostFiles,PostTag,NewPost
from common.forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def save_user(request, form):
    if request.user.is_anonymous():
        try:
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], password = form.cleaned_data['password'])
            isinstance(user, User)
        except:
            return render_to_response('registration/login.html', {'error': Static.USER_ALREADY_EXISTS})
    else:
        user = request.user

    print request.user.is_anonymous()
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    user.groups.add(Group.objects.get(id=2))
    user.save()

    return user

def save_speaker(form):
   profile = UserProfile.objects.create(user=user,
      bio = pf.cleaned_data['bio'],
      presentation=presentation,
      shirtsize=ShirtSize.objects.get(id=pf.cleaned_data['shirt_size']),
      job_title=pf.cleaned_data['job_title'],
      irc_nick=pf.cleaned_data['irc_nick'],
      irc_server=pf.cleaned_data['irc_server'],
      common_channels=pf.cleaned_data['irc_channels'])

def save_volunteer(form):
    role = VolunteerRole.objects.get(id=form.cleaned_data['requested_role'])
#    UserProfile.objects.create(request=role, comments=form.cleaned_data['comments']),)    

def save_user_profile(request, user, type):
    try:
	    profile = user.get_profile()
    except :
	print 'No Profile Found'

    profile = UserProfile.objects.create(user=user,
            bio = '', 
            shirtsize=ShirtSize.objects.get(id=form.cleaned_data['shirt_size']),
            job_title=form.cleaned_data['job_title'],
            irc_nick=form.cleaned_data['irc_nick'], 
            irc_server=form.cleaned_data['irc_server'],
            common_channels=form.cleaned_data['irc_channels'])

    if (type == "volunteer"):
        profile = save_volunteer(request)

    if (type == "speaker"):
        profile = save_speaker(request)

    userinfo = dict()
    userinfo['name']= profile.get_full_name()
    userinfo['email']= profile.email
    print "userinfo: " + str(profile) 
    return userinfo

def test(request):
    volunteer_form = VolunteerForm()
    presenter_form = PresenterForm()
    if request.method == 'POST':
        presenter_form = PresenterForm(request.POST)
    if not presenter_form.is_valid():
        render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})
    return render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})

def index(request):
    posts = NewPost.objects.order_by('display_date')[:10]
    postlist = list()
    for p in posts:
	postdata = dict()
	files = list()
	for f in p.files.get_query_set():
	    fileobj = dict()
	    fileobj['name'] = f.display_name
	    fileobj['fileurl'] = f.file.url
	    files.append(f)
	
	postdata['title'] = p.title
	postdata['content'] = p.content
	postdata['tags'] = p.tags
	postdata['created'] = p.created
	postdata['files'] = files
	postlist.append(postdata)
    
    return render_to_response('index.html',{'posts':postlist,'context_instance':RequestContext(request)})

def contact(request):
    con_form = ContactUsForm()
    if request.method == 'POST':
        con_form = ContactUsForm(request.POST)
    if con_form.is_valid:
        CaptchaRequest.validate(con_form.data['captcha_uid'],con_form.data['captcha_text'])
        admin = User.objects.filter(is_superuser__exact=True)
        for u in admin:
            u.email_user(con_form.data['subject'],con_form.data['message'],'utosc@utosf.org')
        print u.username

        return HttpResponseRedirect('/')
    else:
        captcha = generate_sum_captcha()
        con_form.data = {'captcha_uid':captcha.uid}
        return render_to_response('contactus.html',{'contactform':con_form, 'captcha':captcha})

@login_required
def profile_show(request):
    if request.user.groups.get_query_set().get(id=1) == 'Presenters':
        return render_to_response('profile_papers.html',{'user':request.user})
    elif request.user.groups.get_query_set().get(id=1) == 'Volunteers':
        return render_to_response('profile_volunteers.html',{'user':request.user})
    user_data = request.user
    user_profile = request.user.get_profile()
    user_presentation = user_profile.presentation
    #data = {'audience': user_presentation.audience,
    #'message': 'Hi there',
    #'sender': 'foo@example.com',
    #'cc_myself': True}

    pf = PresenterForm()
    pf.audience = user_presentation.audience
    pf.bio = user_profile.bio
    pf.cat = user_presentation.cat
    pf.email = user_data.email
    pf.first_name = user_data.first_name
    pf.last_name = user_data.last_name
    pf.irc_channels = user_profile.common_channels
    pf.irc_nick = user_profile.irc_nick
    pf.irc_server = user_profile.irc_server
    pf.job_title = user_profile.job_title
    pf.presentation_title = user_presentation.title
    pf.ss = user_profile.shirtsize
    
    if request.user.groups.get_query_set().get(id=1) == 'Presenters':
        return render_to_response('edit_papers.html',{'pf':pf})
    elif request.user.groups.get_query_set().get(id=1) == 'Volunteers':
        return render_to_response('edit_volunteers.html',{'user':request.user})
    return render_to_response('profile.html', None)
    


from common.models import CaptchaRequest
from cStringIO import StringIO
import random
import Image,ImageDraw,ImageFont

def generate_sum_captcha(request_path='any'):
    numbers = (int(random.random()*9)+1,int(random.random()*9)+1)
    print numbers
    text = "%d+%d" % numbers
    answer = sum(numbers)
    return CaptchaRequest.generate_request(text,answer,request_path)

# You need to get the font from somewhere and have it accessible by Django
# I have it set in the djaptcha's settings dir 
from settings import FONT_PATH,FONT_SIZE


def captcha_image(request,token_uid):
    """
    Generate a new captcha image.
    """
    captcha = CaptchaRequest.objects.get(uid=token_uid)
    text = captcha.text
    #TODO: Calculate the image dimensions according to the given text.
    #      The dimensions below are for a "X+Y" text
    image = Image.new('RGB', (40, 23), (39, 36, 81))
    # You need to specify the fonts dir and the font you are going to usue
    font = ImageFont.truetype(FONT_PATH,FONT_SIZE)
    draw = ImageDraw.Draw(image)
    # Draw the text, starting from (2,2) so the text won't be edge
    draw.text((2, 2), text, font = font, fill = (153, 204, 0))
    # Saves the image in a StringIO object, so you can write the response
    # in a HttpResponse object
    out = StringIO()
    image.save(out,"JPEG")
    out.seek(0)
    response = HttpResponse()
    response['Content-Type'] = 'image/jpeg'
    response.write(out.read())
    return response 

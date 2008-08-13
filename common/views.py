# Create your views here.
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
from common.models import User,UserProfile,PostFiles,PostTag,BlogPost,LinkItems
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
    links = LinkItems.objects.order_by('order')
    return HttpResponseRedirect('/pages/home/')

def blog(request):
    links = LinkItems.objects.order_by('innertext')[:10]
    posts = BlogPost.objects.order_by('-display_date')[:10]
    postlist = list()
    for p in posts:
        postdata = dict()
        files = list()
        for f in p.files.get_query_set():
            fileobj = dict()
            fileobj['name'] = f.display_name
            fileobj['fileurl'] = f.file.url
            files.append(f)

        postdata['id'] = p.id
        postdata['title'] = p.title
        postdata['content'] = p.content
        postdata['tags'] = p.tags
        postdata['created'] = p.created
        postdata['files'] = files
    #	postdata['pic'] = p.poster.get_profile().user_photo
        postdata['fullname'] = p.poster.get_full_name()
        postdata['email'] = p.poster.email
        postlist.append(postdata)

    links = LinkItems.objects.order_by('order')
    return render_to_response('blog.html',{'posts':postlist, 'left_links':links}, context_instance=RequestContext(request))

def single_blog_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render_to_response('single_post.html',{'p': post})

def contact(request):
    con_form = ContactUsForm()
    if request.method == 'POST':
        con_form = ContactUsForm(request.POST)
        if con_form.is_valid:
            CaptchaRequest.validate(con_form.data['captcha_uid'],con_form.data['captcha_text'])
            admin = User.objects.filter(is_superuser__exact=True)
            for u in admin:
                u.email_user(con_form.data['subject'],con_form.data['message'],'conference@utos.org')
            print u.username

            return HttpResponseRedirect('/')
    else:
#        captcha = generate_sum_captcha()
        con_form.data = {'captcha_uid':captcha.uid}
        return render_to_response('contactus.html',{'contactform':con_form})

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

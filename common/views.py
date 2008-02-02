# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from common.models import User,UserProfile,Presentation,Category
from common.forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

def test(request):
    volunteer_form = VolunteerForm()
    presenter_form = PresenterForm()
    if request.method == 'POST':
        presenter_form = PresenterForm(request.POST)
        if not presenter_form.is_valid():
            render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})
    return render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})

def login(request):
    if request.method == 'POST':
	login_form = LoginForm(request.POST)
        #username = request.POST['username']
        #password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page
                print "I am redirecting you."
            else:
                # Return disabled account messege
                print "you are disabled"
        else:
            # Return an invalid login error messege
            print "invalid login"
    else:
        return render_to_response('login.html',{'login_form':login_form })

def index(request):
    return render_to_response('index.html',None)

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
	
	return render_to_response('profile_papers.html',{'user':user_loc})
    elif request.user.groups.get_query_set().get(id=1) == 'Volunteers':
	user_loc =request.user
	return render_to_response('profile_volunteers.html',{'user':user_loc})
    
    
    #print request.user
    #print temp
    #print temp.get(id=1)

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

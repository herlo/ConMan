# Create your views here.
from django.shortcuts import render_to_response
from common.models import User,UserProfile,Presentation,Category
from common.forms import *

def test(request):
    volunteer_form = VolunteerForm()
    presenter_form = PresenterForm()
    if request.method == 'POST':
        presenter_form = PresenterForm(request.POST)
        if not presenter_form.is_valid():
            render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})
    return render_to_response('test_template.html',{'volunteer_form':volunteer_form, 'presenter_form':presenter_form})

def index(request):
    return render_to_response('index.html',None)
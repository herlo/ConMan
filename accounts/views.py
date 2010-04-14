from django.conf import settings
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from common.models import *
from django.contrib.auth.models import User
import settings

# Models
from django.contrib.auth.models import User,Group
from accounts.models import UserProfile

# Forms
from accounts.forms import RegistrationForm, ProfileForm, UserForm

def register(request):
    errorMessage = ''
    # no beer and tv make homer something something
    if request.method == 'POST':
        # cheat and fill in the username for the user :D
        reqPOST= request.POST.copy()
        reqPOST['username'] = reqPOST['email']
        regForm = RegistrationForm(reqPOST)

        if regForm.is_valid():
			regForm.save()

    else: 
        regForm = RegistrationForm()
    
    return render_to_response('accounts/registration_form.html',{'form': regForm, 'errorMessage': errorMessage})
    

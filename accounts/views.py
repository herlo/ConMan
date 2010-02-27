from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from common.models import *
import settings

# Models
from django.contrib.auth.models import User,Group
from accounts.models import UserProfile

# Forms
from accounts.forms import RegistrationForm, ProfileForm, UserForm

def register(self):
    # no beer and tv make homer something something
    regForm = RegistrationForm()

    return render_to_response('accounts/registration.html',{'regForm': regForm})
    

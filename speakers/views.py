# Create your views here.
from django.shortcuts import render_to_response
from common.models import *
from common.forms import *
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login
import pdb

def index(request):
    isinstance(request,HttpRequest)
#    pdb.set_trace()
    pf = PresenterForm()
    if request.method == 'POST':
        pf = PresenterForm(request.POST)
        if not pf.is_valid():
            return render_to_response('call_for_papers.html',{'presenter_form':pf})
        else:
            save_user(request, pf)
            save_user_profile(request, user, "speaker")
            try:
                user = authenticate(username=pf.cleaned_data['username'],password=pf.cleaned_data['password'])
            except e:
                return render_to_response('login.html', {'error': e})
            userinfo = dict()
            userinfo['name']= user.get_full_name()
            userinfo['email']= user.email
            return render_to_response('paper_submitted.html',{'user':userinfo})
    else :
        if request.user.is_authenticated():
            isinstance(pf.fields,dict)
            pf.fields.pop('username')
            pf.fields.pop('password')
            pf.fields.pop('confirm_password')
        return render_to_response('call_for_papers.html',{'presenter_form':pf})

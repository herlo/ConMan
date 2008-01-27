# Create your views here.
from django.shortcuts import render_to_response
from common.models import *
from common.forms import *
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User,UserManager,Group
from django.contrib.auth import authenticate,login

def index(request):
    isinstance(request,HttpRequest)
   
        
    pf = PresenterForm()
    if request.method == 'POST':
        pf = PresenterForm(request.POST)
        if not pf.is_valid():
            return render_to_response('call_for_papers.html',{'presenter_form':pf})
        else:
            if request.user.is_anonymous():
               
                user = User.objects.create_user(pf.cleaned_data['username'], pf.cleaned_data['email'], password = pf.cleaned_data['password'])
                isinstance(user, User)
            else:
                user = request.user
                
            user.first_name = pf.cleaned_data['first_name']
            user.last_name = pf.cleaned_data['last_name']
            user.save()
            user.groups.add(Group.objects.get(id=1))
            profile = None
            try:
                profile = user.get_profile()
            except :
                print 'No Profile Found'
            
            category = Category.objects.get(id=pf.cleaned_data['category'])
            presentation = Presentation.objects.create(cat=category, audience=AudienceType.objects.get(id=pf.cleaned_data['audience']), abstract=pf.cleaned_data['short_abstract'], 
                                                       longabstract="",status='Pending', title=pf.cleaned_data['presentation_title'])
            
            profile = UserProfile.objects.create(user=user,
                                                     bio = pf.cleaned_data['bio'],
                                                     presentation=presentation,
                                                     shirtsize=ShirtSize.objects.get(id=pf.cleaned_data['shirt_size']),
                                                     job_title=pf.cleaned_data['job_title'],
                                                     irc_nick=pf.cleaned_data['irc_nick'],
                                                     irc_server=pf.cleaned_data['irc_server'],
                                                     common_channels=pf.cleaned_data['irc_channels'])
            user2 =authenticate(username=pf.cleaned_data['username'],password=pf.cleaned_data['password'])
            userinfo = dict()
            userinfo['name']= user2.get_full_name()
            userinfo['email']= user2.email
            
            return render_to_response('paper_submitted.html',{'user':userinfo})
            
    else :
        if request.user.is_authenticated():
            isinstance(pf.fields,dict)
            pf.fields.pop('username')
            pf.fields.pop('password')
            pf.fields.pop('confirm_password')
        return render_to_response('call_for_papers.html',{'presenter_form':pf})
    

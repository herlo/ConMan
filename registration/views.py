"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from common.models import *

from registration.forms import RegistrationForm, ProfileForm
from registration.models import RegistrationProfile


def activate(request, activation_key, template_name='registration/activate.html'):
    """
    Activates a ``User``'s account, if their key is valid and hasn't
    expired.
    
    By default, uses the template ``registration/activate.html``; to
    change this, pass the name of a template as the keyword argument
    ``template_name``.
    
    **Context:**
    
    account
        The ``User`` object corresponding to the account, if the
        activation was successful. ``False`` if the activation was not
        successful.
    
    expiration_days
        The number of days for which activation keys stay valid after
        registration.
    
    **Template:**
    
    registration/activate.html or ``template_name`` keyword argument.
    
    """
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    return render_to_response(template_name,
                              { 'account': account,
                                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=RequestContext(request))


def make_basic_profile(user=None):
    isinstance(user,User)
    up = UserProfile(user=user)
    up.user = user
    up.save();

def update_profile(user, form, photo):
    isinstance(user,User)
    up = user.get_profile()
    up.bio = form.cleaned_data['bio']
    
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    up.shirt_size = form.cleaned_data['shirt_size']
    print form.cleaned_data['shirt_size']
    up.job_title = form.cleaned_data['job_title']
    up.irc_nick = form.cleaned_data['irc_nick']
    up.irc_server = form.cleaned_data['irc_server']
    up.common_channels = form.cleaned_data['irc_channels']
    up.site = form.cleaned_data['web_site']
    up.save_user_photo_file(user.username+'.'+photo['filename'].split('.')[len(photo['filename'].split('.'))-1] ,photo['content'])
    up.save()
    user.save()

@login_required
def profile(request, success_url='/speaker/papers/', 
              form_class=ProfileForm, profile_callback=update_profile, 
              template_name='registration/profile_form.html'):
    links = LinkItems.objects.order_by('order')
    form = form_class()
    if request.method == 'POST':
        pdata = request.POST.copy()
        pdata.update(request.FILES)
        form = form_class(pdata)
        if form.is_valid():
            user = User.objects.get(id=request.session.get('_auth_user_id'))
            #user.get_profile().save_photo_file(request.FILES['photo']['filename'],request.FILES['photo']['content'])
            update_profile(user, form, request.FILES['photo'])
            return HttpResponseRedirect(success_url)
    else:
        user = User.objects.get(id=request.session.get('_auth_user_id'))
        usp = user.get_profile()

        if user.first_name:
    
            up = dict()
            xp = dict()

            up['username'] = user.username
            up['first_name'] = user.first_name
            up['last_name'] = user.last_name
            up['job_title'] = usp.job_title
            up['bio'] = usp.bio
            up['web_site'] = usp.site
            up['shirt_size'] = usp.shirt_size.id

            up['irc_nick'] = usp.irc_nick
            up['irc_server'] = usp.irc_server
            up['irc_channels'] = usp.common_channels
            up['photo'] = usp.user_photo
            form = form_class(up)
    return render_to_response(template_name,
                              { 'form': form, 'left_links':links },
                              context_instance=RequestContext(request))
    

def register(request, success_url='/accounts/register/complete/',
             form_class=RegistrationForm, profile_callback=make_basic_profile,
             template_name='registration/registration_form.html'):
    """
    Allows a new user to register an account.
    
    Following successful registration, redirects to either
    ``/accounts/register/complete/`` or, if supplied, the URL
    specified in the keyword argument ``success_url``.
    
    By default, ``registration.forms.RegistrationForm`` will be used
    as the registration form; to change this, pass a different form
    class as the ``form_class`` keyword argument. The form class you
    specify must have a method ``save`` which will create and return
    the new ``User``, and that method must accept the keyword argument
    ``profile_callback`` (see below).
    
    To enable creation of a site-specific user profile object for the
    new user, pass a function which will create the profile object as
    the keyword argument ``profile_callback``. See
    ``RegistrationManager.create_inactive_user`` in the file
    ``models.py`` for details on how to write this function.
    
    By default, uses the template
    ``registration/registration_form.html``; to change this, pass the
    name of a template as the keyword argument ``template_name``.
    
    **Context:**
    
    form
        The registration form.
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            new_user = form.save(profile_callback=profile_callback)
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    links = LinkItems.objects.order_by('order')
    return render_to_response(template_name,
                              { 'form': form, 'left_links':links },
                              context_instance=RequestContext(request))

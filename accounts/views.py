"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from common.models import *

from accounts.forms import RegistrationForm, ProfileForm
from accounts.models import RegistrationProfile


def activate(request, activation_key, template_name='accounts/activate.html'):
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

def update_profile(user, form, photo=None):
    isinstance(user,User)
    try:
        up = user.get_profile()
    except UserProfile.DoesNotExist:
        up = UserProfile.objects.create(user=user)

    up.bio = form.cleaned_data['bio']
    
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    up.shirt_size = form.cleaned_data['shirt_size']
    #print form.cleaned_data['shirt_size']
    up.job_title = form.cleaned_data['job_title']
    up.company = form.cleaned_data['company']
    up.irc_nick = form.cleaned_data['irc_nick']
    up.irc_server = form.cleaned_data['irc_server']
    up.common_channels = form.cleaned_data['irc_channels']
    up.site = form.cleaned_data['web_site']
    if (photo):
        up.save_user_photo_file(user.username+'.'+photo['filename'].split('.')[len(photo['filename'].split('.'))-1] ,photo['content'])
    up.save()
    user.save()

@login_required
def profile(request, success_url='/pages/home/', 
              form_class=ProfileForm, profile_callback=update_profile, 
              template_name='accounts/profile_form.html'):
    photo_url = ''
    form = form_class()
    if request.method == 'POST':
        pdata = request.POST.copy()
        pdata.update(request.FILES)
        form = form_class(pdata)
        if form.is_valid():
            #user.get_profile().save_photo_file(request.FILES['photo']['filename'],request.FILES['photo']['content'])
            update_profile(request.user, form, request.FILES.get('photo', None))
            return HttpResponseRedirect(success_url)
    else:
        try:
            usp = request.user.get_profile()
        except UserProfile.DoesNotExist:
            usp = UserProfile.objects.create(user=request.user)

        # make a dict from the UserProfile and User objects for initial data for ProfileForm
        initial_dict = dict(request.user.__dict__, **usp.__dict__)
        # explicit mappings for UserProfile fields that don't match the ProfileForm field names
        initial_dict['irc_channels'] = usp.common_channels
        initial_dict['web_site'] = usp.site
        initial_dict['photo'] = usp.user_photo
        # somehow some UserProfiles are missing shirt_size, possibly from a db migration
        try:
            initial_dict['shirt_size'] = usp.shirt_size.id
        except AttributeError:
            pass

        if request.user.first_name:
            form = form_class(initial=initial_dict)
            photo_url =  settings.HOST_NAME + settings.MEDIA_URL + str(usp.user_photo)

    return render_to_response(template_name,
            {'form': form, 'photo_url': photo_url, 'left_links':None},
            context_instance=RequestContext(request))

def register(request, success_url='/accounts/register/complete/',
             form_class=RegistrationForm, profile_callback=make_basic_profile,
             template_name='accounts/registration_form.html'):
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
    return render_to_response(template_name,
                              { 'form': form},
                              context_instance=RequestContext(request))

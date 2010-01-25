"""
Views which allow users to create and activate accounts.

"""

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group

from accounts.forms import RegistrationForm, ProfileForm, UserForm
from accounts.models import RegistrationProfile

from common.models import *
import settings


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


@login_required
def profile(request, success_url='/accounts/profile/',
              form_class=ProfileForm,
              template_name='accounts/profile_form.html'):
    usp = UserProfile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=usp)
        user_form = UserForm(request.POST, instance=request.user)
        forms = (form, user_form)

        if not False in [i.is_valid() for i in forms]:
            for i in forms:
                i.save()

            return HttpResponseRedirect(success_url)
    else:
        form = form_class(instance=usp)
        user_form = UserForm(instance=request.user)

    return render_to_response(template_name, {
        'form': form, 'user_form': user_form, 'profile': usp,
        'left_links':None
        }, context_instance=RequestContext(request))

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
            # this is will make voting work for anyone as long as the
            # Voter group has voting rights
            if settings.ALL_CAN_VOTE:
                group = Group.objects.get(name='Voter')
                new_user.groups.add(group)
                new_user.save()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    return render_to_response(template_name,
                              { 'form': form},
                              context_instance=RequestContext(request))

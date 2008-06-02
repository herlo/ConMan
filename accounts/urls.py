"""
URLConf for Django user registration.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/accounts/'.

"""


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from accounts.views import activate, register, profile

from common.models import LinkItems


#links = dict()
#for link in LinkItems.objects.all().order_by('order'):
#  links[link.href] = link.innertext
  
urlpatterns = patterns('',
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$', activate, name='registration_activate'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'accounts/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'index.html'}, name='auth_logout'),
    url(r'^password/change/$', auth_views.password_change,
        {'template_name': 'accounts/password_change.html'},
        name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
        {'template_name': 'accounts/password_change_done.html'},
        name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset,
        {'template_name': 'accounts/password_reset.html',
            'email_template_name': 'accounts/password_reset_email.html'},
        name='auth_password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        {'template_name': 'accounts/password_reset_done.html'},
        name='auth_password_reset_done'),
    url(r'^register/$', register, name='register'),
    url(r'^register/complete/$', direct_to_template,
        {'template': 'accounts/registration_complete.html'},
        name='registration_complete'),
    url(r'^profile/$', profile, name='profile_form'),
)

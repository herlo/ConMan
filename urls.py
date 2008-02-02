from django.conf.urls.defaults import *
from django.contrib import databrowse

urlpatterns = patterns('',
    # Example:
    # (r'^conman/', include('conman.foo.urls')),
    #(r'^databrowse/(.*)', databrowse.site.root),
    # Uncomment this for admin:
    #Login page
    #(r'^login/', 'common.views.login'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^captcha/(?P<token_uid>\w+).jpg$','common.views.captcha_image'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^testtemplate/', 'common.views.test'),
    (r'^volunteer/$', 'volunteers.views.index'),
    (r'^profile/$', 'common.views.profile_show'),
    #(r'^volunteer/submitted/$', 'volunteers.views.submitted'),
    (r'^speaker/$', 'speakers.views.index'),
       (r'^contact/$', 'common.views.contact'),
    (r'$', 'common.views.index'),
 
    #(r'^speaker/submitted/$', 'speakers.views.submitted'),
    
)
#from django.contrib import databrowse
#from common.models import *

#databrowse.site.register(UserProfile)
#databrowse.site.register(Category)
#databrowse.site.register(VolunteerRole)
#databrowse.site.register(Volunteer)
#databrowse.site.register(Presentation)

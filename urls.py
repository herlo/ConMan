from django.conf.urls.defaults import *
from django.contrib import databrowse

urlpatterns = patterns('',
    # Example:
    # (r'^conman/', include('conman.foo.urls')),
    #(r'^databrowse/(.*)', databrowse.site.root),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^testtemplate/', 'common.views.test'),
    (r'^volunteer/', 'volunteers.views.index'),
    #(r'^volunteer/submitted/', 'volunteers.views.submitted'),
    (r'^speaker/$', 'speakers.views.index'),
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

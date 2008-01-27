from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^conman/', include('conman.foo.urls')),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^testtemplate/', include('common.views.test')),
)


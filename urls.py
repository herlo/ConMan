from django.contrib import databrowse
from django.conf.urls.defaults import *
from common.models import LatestEntries #, LatestEntriesByCategory

feeds = {
    'latest': LatestEntries,
#    'categories': LatestEntriesByCategory,
#    'author': LatestEntriesByAuthor,
}

urlpatterns = patterns('',
    # Example:
    # (r'^conman/', include('conman.foo.urls')),
    #(r'^databrowse/(.*)', databrowse.site.root),
    # Uncomment this for admin:
    #Login page
    #(r'^login/', 'common.views.login'),
    #(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
#    (r'^captcha/(?P<token_uid>\w+).jpg$','common.views.captcha_image'),
#    (r'^contact/$', 'common.views.contact'),
#    (r'^testtemplate/$', 'common.views.test'),
#    (r'^blog/$', 'common.views.index'),
#    (r'^post/(?P<post_id>\d+)/$', 'common.views.single_blog_post'),

    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^accounts/', include('registration.urls')),
#    (r'^profile/$', 'common.views.profile_show'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^volunteer/$', 'volunteers.views.index'),
    (r'^speaker/papers/(?P<abs_id>\d+)?/?$', 'speakers.views.abstract'),
    (r'^speaker/papers/delete/(?P<abs_id>\d+)/$', 'speakers.views.delete_abstract'),
#    (r'^speaker/$', 'speakers.views.index'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'$', 'common.views.index'),
)

#from django.contrib import databrowse
#from common.models import *

#databrowse.site.register(UserProfile)
#databrowse.site.register(Category)
#databrowse.site.register(VolunteerRole)
#databrowse.site.register(Volunteer)
#databrowse.site.register(Presentation)

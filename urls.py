from django.contrib import databrowse
from django.conf.urls.defaults import *
from common.models import LatestEntries #, LatestEntriesByCategory

feeds = {
    'latest': LatestEntries,
#    'categories': LatestEntriesByCategory,
#    'author': LatestEntriesByAuthor,
}

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^accounts/', include('registration.urls')),
#    (r'^profile/$', 'common.views.profile_show'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^volunteer/$', 'volunteers.views.index'),
    (r'^speaker/papers/(?P<abs_id>\d+)?/?$', 'speakers.views.abstract'),
    (r'^speaker/papers/(?P<abs_id>\d+)/delete/$', 'speakers.views.delete_abstract'),
#    (r'^pages/(?P<fp_id>\d+)/$', 'common.views.show_flatpage'),
#    (r'^speaker/$', 'speakers.views.index'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^$', 'common.views.index'),
)


from django.contrib import databrowse
from django.conf.urls.defaults import *
from voting.views import vote_on_object
from django.contrib.auth.decorators import user_passes_test
from speakers.models import Presentation
from django.contrib.auth.models import User,Group
from django.contrib import admin
from django.conf.urls.defaults import *
from speakers.feeds import LatestEntries

#from common import admin

feeds = {
    'latest': LatestEntries,
#    'categories': LatestEntriesByCategory,
}

admin.autodiscover()

presentation_dict = {
    'model': Presentation,
    'template_object_name': 'presentation',
    'allow_xmlhttprequest': True,
}
can_vote = user_passes_test(lambda u: u.has_perm('voting.add_vote'), login_url='/admin/')

urlpatterns = patterns('',
    (r'^admin/speakers/presentation/voting-results/$', 'speakers.views.voting_results'),
    (r'^admin/speakers/show/$', 'speakers.views.show_speakers_admin'),
#    (r'^admin/speakers/mass_email/$', 'common.views.mass_email', {'users': User.objects.all() }),
    (r'^admin/(.*)', admin.site.root),

#    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^feeds/speaker/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^accounts/', include('accounts.urls')),
    (r'^about/tos/$', 'common.views.show_tos'),
#    (r'^profile/$', 'common.views.profile_show'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^speaker/papers/(?P<abs_id>\d+)?/?$', 'speakers.views.abstract'),
    (r'^speaker/papers/(?P<abs_id>\d+)/delete/$', 'speakers.views.delete_abstract'),
    (r'^speaker/list/(?P<status>\w+)?/?$', 'speakers.views.show_speakers'),
    (r'^speaker/(?P<s_id>\d+)/$', 'speakers.views.speaker_info'),
#    (r'^presentation/schedule/(?P<day>\w+)?/?$', 'speakers.views.show_presentation_schedule'),
    (r'^presentation/schedule/(?P<day>\d{4}-\d{2}-\d{2})?/?$', 'speakers.views.show_presentation_schedule'),
    (r'^presentation/(?P<p_id>\d+)/$', 'speakers.views.show_presentation'),
    (r'^presentation/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', can_vote(vote_on_object), presentation_dict),
    (r'^sponsor/list/$', 'sponsors.views.index'),
    (r'^lug/list/$', 'lugs.views.index'),
# volunteer stuff
    (r'^volunteer/$', 'volunteers.views.index'),
    (r'^volunteer/list/$', 'volunteers.views.list'),
    (r'^volunteer/(?P<vol_id>\d+)?/?$', 'volunteers.views.manage'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    (r'^$', 'common.views.index'),
)

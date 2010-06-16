from django.conf import settings
from django.contrib.sites.models import Site

from common.models import Option
 
class SiteIdOnFlyMiddleware:

    '''This class will allow dynamic site decisions based upon 
        the HTTP_HOST value of the request.  It might be a good
        idea to cache this value or set a cookie since it's only 
        a one time deal at the initiation of a session.'''

    def process_request(self, request):
        host = request.META.get('HTTP_HOST').split(':')[0]

        try:
            site = Site.objects.get(domain=host)
            settings.SITE_ID = site.id
        except:
            settings.SITE_ID = 1



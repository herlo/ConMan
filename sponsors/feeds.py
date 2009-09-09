from django.contrib.syndication.feeds import Feed
import settings
from sponsors.models import Sponsor,Level

class SponsorList(Feed):
    title = "UTOSC 2009 Sponsors"
    link = "/speaker/list/all/"
    description = "Sponsors for UTOSC 2009"

    def items(self):
        return Sponsor.objects.all().order_by('level')

    def item_link(self, item):
        return item.url

    def item_enclosure_url(self, item):
        item_enclosure_url = settings.MEDIA_URL + item.lg_logo.url




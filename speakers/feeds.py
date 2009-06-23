from django.contrib.syndication.feeds import Feed
from speakers.models import Presentation

class LatestEntries(Feed):
    title = "UTOSC 2009 Latest Abstracts"
    link = "/speaker/list/all/"
    description = "Latest abstract submissions for UTOSC 2009."

    def items(self):
        return Presentation.objects.all()




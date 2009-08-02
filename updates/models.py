from django.db import models
from django.contrib.auth.models import User
import datetime
import settings
if settings.TWITTER_ENABLED:
    import twitter

# Used to update what's going on before / during / after the conference.
# Would like to enable more than twitter, but that's what we've got so far

class Update(models.Model):

    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(max_length=500,blank=True,null=True,help_text="No more than 500 characters")
    link_title = models.CharField(max_length=25,blank=True,null=True,help_text="Something like 'Read More'")
    link_url = models.CharField(max_length=150,blank=True,null=True,help_text="An existing url about this update")
    social_info = models.CharField(max_length=140,blank=True,null=True,help_text="Tell the world something in 140 characters. Probably a short version of description")
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)
    author = models.ForeignKey(User)
    
    def save(self):
        if not self.id:
            self.created = datetime.date.today()
            # add twitter code here (soon ping.fm)
            # we want it to succeed, but if it doesn't, oh well!
            if settings.TWITTER_ENABLED and self.social_info:
                twit = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
                twit.PostUpdate(self.social_info)
        self.updated = datetime.datetime.today()
        super(Update, self).save()


    def __unicode__(self):
        return self.name



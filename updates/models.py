from django.db import models
from django.contrib.auth.models import User
import datetime
import twitter
import settings

# Create your models here.
# Used to update what's going on before / during / after the conference.
# could be used to update social networks too

class Update(models.Model):

    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(max_length=140,blank=True,null=True)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)
    author = models.ForeignKey(User)
    
    def save(self):
        if not self.id:
            self.created = datetime.date.today()
            # add twitter code here (soon ping.fm)
            # we want it to succeed, but if it doesn't, oh well!
            twit = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
            twit.PostUpdate(self.description)
        self.updated = datetime.datetime.today()
        super(Update, self).save()


    def __unicode__(self):
        return self.name



from django.db import models
from django.contrib.auth.models import User
import datetime
import settings
import urllib
import urllib2

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
            if settings.PINGFM_ENABLED:
                post_uri = settings.PINGFM +'user.post'
                params = {}
                params['body'] = self.description
                params['user_app_key'] = settings.PINGFM_USER_KEY
                params['api_key'] = settings.PINGFM_APP_KEY
                params['post_method'] = 'default'
                post_params = urllib.urlencode(params)
                post_response = urllib2.urlopen(post_uri, post_params).read()
                # at this point we should check for failure or success, but as herlo noted "oh well!"
                
        self.updated = datetime.datetime.today()
        super(Update, self).save()


    def __unicode__(self):
        return self.name



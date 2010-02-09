from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.models import Site

from common.config import Static
from datetime import datetime,timedelta
from random import random
import sha

from settings import TIMEOUT

SHIRT_SIZES = (
    ('S', 'Small'),
    ('XS', 'Extra-Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('2XL', 'XX Large'),
    ('3XL', 'XXX Large'),
    ('4XL', 'IV Large'),
    ('5XL', 'V Large'),
)

def normalize_photo_name(instance, filename):
    """Renames avatar image to match the username."""
    return u'img/user_photos/%s_avatar.%s' % (
            instance.user.username, filename.split('.')[-1])

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        """Overwrite an existing file on the filesystem."""
        if self.exists(name):
            self.delete(name)
        return name

class ShirtSize(models.Model):

    name = models.CharField(max_length=50, choices=SHIRT_SIZES)
    def __unicode__(self):
        return self.get_name_display()

#    class Admin:
#        list_display = ('id', 'name',)

class UserProfile(models.Model):

#    volunteerinfo = models.ForeignKey(Volunteer, null=True, blank=True,edit_inline=models.STACKED,num_extra_on_change=1)
    #presentation = models.ForeignKey(Presentation, null=True, blank=True,)
    user = models.ForeignKey(User,unique=True)

    bio = models.TextField(null=True, blank=True)
    shirt_size = models.ForeignKey(ShirtSize, null=True,blank=True)
    job_title = models.CharField(max_length=200, null=True, blank=True, db_index=True,)
    company = models.CharField(max_length=200, null=True, blank=True, db_index=True,)
    irc_nick = models.CharField(max_length=100, null=True, blank=True, db_index=True,)
    irc_server = models.CharField(max_length=150, null=True, blank=True, db_index=True,)
    common_channels = models.CharField(max_length=500, null=True, blank=True, db_index=True,)
    user_photo = models.ImageField(upload_to=normalize_photo_name, storage=OverwriteStorage(), null=True, blank=True,)
    site = models.URLField(db_index=True, blank=True, null=True,)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Theme(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)
    preview = models.ImageField(blank=True,null=True,upload_to='theme_preview/')

    def __unicode__(self):
        return '%s' % self.name

class Option(models.Model):
    site = models.ForeignKey(Site)
    theme = models.ForeignKey(Theme)

    def __unicode__(self):
        return '%s' % self.site.name

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.models import Site

from common.config import Static
from datetime import datetime,timedelta
from random import random
import sha

from settings import TIMEOUT

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

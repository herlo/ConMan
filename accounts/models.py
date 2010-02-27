from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=5, blank=True)
    phoneHome = models.CharField('Phone Number', max_length=10, blank=True, help_text='(XXX) XXX-XXXX')
    phoneWork = models.CharField('Work Number', max_length=10, blank=True, help_text='(XXX) XXX-XXXX')
    phoneCell = models.CharField('Cell Number', max_length=10, blank=True, help_text='(XXX) XXX-XXXX')
    jobTitle = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=50, blank=True)
    referral = models.CharField(max_length=50, blank=True)
    bio = models.TextField(null=True, blank=True)
    ircNick = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    ircServer = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    commonChannels = models.CharField(max_length=500, null=True, blank=True, db_index=True)

# work this back in later
#    userPhoto = models.ImageField(upload_to=normalize_photo_name, storage=OverwriteStorage(), null=True, blank=True)

    url = models.URLField(db_index=True, blank=True, null=True)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


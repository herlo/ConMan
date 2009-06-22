from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
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
    '''
      >>> size = ShirtSize(name="2XL")
      >>> size.get_name_display()
      'XX Large'
    '''
    name = models.CharField(max_length=50, choices=SHIRT_SIZES)
    def __unicode__(self):
        return self.get_name_display()

#    class Admin:
#        list_display = ('id', 'name',)

class UserProfile(models.Model):    
    '''

      >>> from django.contrib.auth.models import User

    Create a User
      >>> userMan = User.objects.create_user('Janx', 'lennon@thebeatles.com')

    Create the category and audience for the presentation
      >>> Category.objects.create(name="Crapology")
      <Category: Crapology>
      >>> AudienceType.objects.create(name="For Experts Only")
      <AudienceType: For Experts Only>

    Create a presentation for the user
      >>> present = Presentation.objects.create(
      ... cat=Category.objects.get(id=1),
      ... audience=AudienceType.objects.get(id=1),
      ... abstract="crapology in a nutshell",
      ... longabstract="To enlighten on the subject of crap"
      ... )

    Create a shirtSize for the user
      >>> shirt = ShirtSize.objects.create(name="XXXXS")

    Create a VolunteerRole for the volunteer
      >>> VolunteerRole.objects.create(name="Fun Sucker")
      <VolunteerRole: Fun Sucker>

    Create a volunteer with the user

      >>> vol = Volunteer.objects.create(
      ... role=VolunteerRole.objects.get(id=1),
      ... request=VolunteerRole.objects.get(id=1),
      ... comments="This is my comment")

      >>> userProfile = UserProfile(
      ... user=userMan,
      ... bio="I am the best in my field",
      ... presentation=present,
      ... shirtsize=shirt,
      ... volunteerinfo=vol,
      ... job_title="The master of the universe of crap",
      ... irc_nick="CrapMaster",
      ... irc_server="FreeNode",
      ... common_channels="#crapology, #shitonomics")


      >>> userProfile
      <UserProfile: Janx's profile>
      >>> userProfile.user
      <User: Janx>
      >>> userProfile.bio
      'I am the best in my field'
      >>> userProfile.presentation
      <Presentation:  Presentation 2>
      >>> userProfile.shirtsize
      <ShirtSize: XXXXS>
      >>> userProfile.volunteerinfo
      <Volunteer: Fun Sucker Volunteer 1>
      >>> userProfile.job_title
      'The master of the universe of crap'
      >>> userProfile.irc_nick
      'CrapMaster'
      >>> userProfile.irc_server
      'FreeNode'
      >>> userProfile.common_channels
      '#crapology, #shitonomics'

    '''

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

#    class Admin:
#        search_fields = ['job_title','common_channels','@bio','site']
#        list_display = ('user', 'irc_nick', 'common_channels')
#        fields = (
#            (None, {
#                'fields': ('user', 'bio', 'job_title', 'site')
#            }),
#            ('Presentations', {
#                'classes': 'collapse',
#                'fields' : ('presentation')
#            }),
#            ('Volunteer Info', {
#                'classes': 'collapse',
#                'fields' : ('volunteer_info')
#            }),
#            ('Photo', {
#                'classes': 'collapse',
#                'fields' : ('user_photo')
#            }),
#            ('Misc Info', {
#                'classes': 'collapse',
#                'fields' : ('shirt_size', 'irc_nick', 'irc_server', 'common_channels')
#            }),
#        )


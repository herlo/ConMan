from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from random import random
import sha

from settings import TIMEOUT

AUDIENCE_CHOICES = (
    ('BUS', 'Business'),
    ('TEK', 'Technical'),
    ('EDU', 'Educational'),
)

VOLUNTEER_CHOICES = (
    ('RMGR', 'Room Manager'),
    ('USH', 'Usher'),
    ('GRT', 'Greeter'),
    ('HRT', 'Heartsbane'),
    ('TEK', 'Technician'),
)

SHIRT_SIZES = (
    ('S', 'Small'),
    ('XS', 'Extra-Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'XX Large'),
    ('XXXL', 'XXX Large'),
)

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Denied', 'Denied'),
    ('Alternate', 'Alternate'),
    ('Approved', 'Approved'),
)

# Create your models here.    
class Category(models.Model):
    '''
    >>> c = Category(name="hot_or_not")
    >>> c.name
    'hot_or_not'
    '''
    name = models.CharField(max_length=150,db_index=True)
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass
    
    class Meta:
        verbose_name_plural = "Categories"
    
class AudienceType(models.Model):
    '''
    >>> a = AudienceType(name="Legendary")
    >>> a.name
    'Legendary'
    '''
    name = models.CharField(max_length=150, db_index=True)
    def __unicode__(self):
        return self.name
    class Admin:
        pass
    
class ShirtSize(models.Model):
    '''
      >>> size = ShirtSize(name="XXL")
      >>> size.name
      'XXL'
    '''
    name = models.CharField(max_length=150, db_index=True)
    def __unicode__(self):
        return self.name
    class Admin:
        pass

class VolunteerRole(models.Model):
    '''
    >>> v = VolunteerRole(name = "killa")
    >>> v.name
    'killa'
    '''
    name = models.CharField(max_length=150, db_index=True)
    def __unicode__(self):
        return self.name
    class Admin:
        pass

class Volunteer(models.Model):
    '''
    Create a VolunteerRole for the user
      >>> VolunteerRole.objects.create(name="Fun Sucker")
      <VolunteerRole: Fun Sucker>

    Create a volunteer with the first default role value
      >>> v = Volunteer.objects.create(
      ... role=VolunteerRole.objects.get(id=1),
      ... request=VolunteerRole.objects.get(id=1),
      ... comments="This is my comment")

      >>> v
      <Volunteer: Fun Sucker Volunteer 2>
      >>> v.role
      <VolunteerRole: Fun Sucker>
      >>> v.request
      <VolunteerRole: Fun Sucker>
      >>> v.comments
      'This is my comment'
    '''
    #role = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    #request = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    role = models.ForeignKey(VolunteerRole,related_name='role',blank=True, null=True)
    request = models.ForeignKey(VolunteerRole, related_name='request')
    comments = models.TextField()
    
    def __unicode__(self):
        return self.role.name + " Volunteer " + str(self.pk)
    class Admin:
        list_filter = ['role','request']

class Presentation(models.Model):
    '''
    Create the category and audience for the presentation
      >>> Category.objects.create(name="Crapology")
      <Category: Crapology>
      >>> AudienceType.objects.create(name="For Experts Only")
      <AudienceType: For Experts Only>

      >>> p = Presentation.objects.create(
      ... cat=Category.objects.get(id=1),
      ... audience=AudienceType.objects.get(id=1),
      ... abstract="crapology in a nutshell",
      ... longabstract="To enlighten on the subject of crap",
      ... status='pending',
      ... title='Come listen to crap'
      ... )

      >>> p
      <Presentation:  Presentation 1>
      >>> p.cat
      <Category: Crapology>
      >>> p.audience
      <AudienceType: For Experts Only>
      >>> p.abstract
      'crapology in a nutshell'
      >>> p.longabstract
      'To enlighten on the subject of crap'
      >>> p.status
      'pending'
      >>> p.title
      'Come listen to crap'
    '''
    cat = models.ForeignKey(Category)
    audience = models.ForeignKey(AudienceType)
   # audience = models.CharField(max_length=200, choices=AUDIENCE_CHOICES,db_index=True)
    abstract = models.CharField(max_length=500)
    longabstract = models.TextField()
    status = models.CharField(max_length=70,choices=STATUS_CHOICES,db_index=True)
    title = models.CharField(max_length=150, db_index=True)
    slides = models.FileField(upload_to="slides",blank=True,null=True)

    
    def __unicode__(self):
        return " Presentation " + str(self.pk)
    class Admin:
        list_filter = ['cat','audience','status']
	list_display = ('title','abstract', 'status')
	search_fields = ['@longabstract','status','@title','foreign_key__cat']

    
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

    user = models.ForeignKey(User,unique=True)
    bio = models.TextField()
    presentation = models.ForeignKey(Presentation, blank=True)
    #shirtsize = models.CharField(max_length=200, db_index=True, choices=SHIRT_SIZES)
    shirtsize = models.ForeignKey(ShirtSize)
    volunteerinfo = models.ForeignKey(Volunteer, blank=True)
    job_title = models.CharField(max_length=200, db_index=True)
    irc_nick = models.CharField(max_length=100, db_index=True)
    irc_server = models.CharField(max_length=150, db_index=True)
    common_channels = models.CharField(max_length=500, db_index=True)
    user_photo = models.ImageField(width_field=500,height_field=500,upload_to='user_photos',null=True,blank=True)
    site = models.URLField(db_index=True, blank=True)
    
    def __unicode__(self):
        return str(self.user)  + "'s profile" 
    
    class Admin:
        pass

class PostTag(models.Model):
    name = models.CharField(max_length=150,db_index=True)
    created = models.DateTimeField()
    
    class Admin:
        pass
    
class PostFiles(models.Model):
    display_name = models.CharField(max_length=300,db_index=True)
    upload_date = models.DateTimeField(db_index=True)
    uploader = models.ForeignKey(User)
    posts = models.ManyToManyField('NewPost')
    file = models.FileField(upload_to="post_files")

    class Admin:
        pass
class NewPost(models.Model): 
    poster = models.ForeignKey(User)
    created = models.DateTimeField(db_index=True)
    display_date = models.DateTimeField(db_index=True)
    tags = models.ManyToOneRel(PostTag,'Tag',edit_inline=True)
    files = models.ManyToManyField(PostFiles,blank=True, null=True)
    content = models.TextField()
    title = models.CharField(max_length=200,db_index=True)
    class Admin:
        pass

    
def future_datetime(**kw_args):
	def on_call():
		return datetime.now()+timedelta(**kw_args)
	return on_call
	
CAPTCHA_ANSWER_OK = 1 
CAPTCHA_UID_NOT_FOUND = -1
CAPTCHA_REQUEST_EXPIRED = -2
CAPTCHA_WRONG_ANSWER = -3

class CaptchaRequest(models.Model):
    """"
    A Captcha request, used to avoid spamming in comments and such
    Each request is valid for 15 minutes (you can change the value in the valid_until field)
    """
    
    valid_until = models.DateTimeField(default=future_datetime(minutes=TIMEOUT))
    answer = models.IntegerField()
    request_path = models.CharField(max_length=50,blank=True)
    uid = models.CharField(max_length=40,blank=True)
    text = models.CharField(max_length=10)

    def save(self):
        shaobj = sha.new()
        # You can add anything you want here, if you're *really* serious
        # about an UID. This should be enough though
        shaobj.update(self.request_path)
        shaobj.update(str(random()))
        shaobj.update(str(datetime.now()))
        shaobj.update(str(self.valid_until))
        shaobj.update(str(self.answer))
        self.uid = shaobj.hexdigest()
        super(CaptchaRequest,self).save()

    @staticmethod
    def clean_expired():
        [x.delete() for x in CaptchaRequest.objects.filter(valid_until__lt=datetime.now())]

    @staticmethod
    def validate(request_uid,given_answer):
        result_list = CaptchaRequest.objects.filter(uid=request_uid)
        result = None
        if len(result_list)>0:
            result = result_list[0]
        if not result:
            return CAPTCHA_UID_NOT_FOUND
        if result.valid_until<datetime.now():
            result.delete()
            return CAPTCHA_REQUEST_EXPIRED 
        if result.answer!=given_answer:
            result.delete()
            return CAPTCHA_WRONG_ANSWER
        result.delete()
        return CAPTCHA_ANSWER_OK
    
    @staticmethod
    def generate_request(text,answer,request_path='any'):
	    """
	    Generate a new captcha request. This creates 
	    """
	    captcha = CaptchaRequest(text=text,request_path=request_path,answer=answer)
	    captcha.save()
	    return captcha

	

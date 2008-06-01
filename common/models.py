from django.db import models
from django.contrib.auth.models import User
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

class ShirtSize(models.Model):
    '''
      >>> size = ShirtSize(name="2XL")
      >>> size.get_name_display()
      'XX Large'
    '''
    name = models.CharField(max_length=50, choices=SHIRT_SIZES)
    def __unicode__(self):
        return self.get_name_display()

    class Admin:
        list_display = ('id', 'name',)

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
    user = models.ForeignKey(User,unique=True,core=True)
    bio = models.TextField(null=True, blank=True,core=True)

    shirt_size = models.ForeignKey(ShirtSize,core=True, null=True,blank=True)
    job_title = models.CharField(max_length=200, null=True, blank=True, db_index=True,core=True)
    company = models.CharField(max_length=200, null=True, blank=True, db_index=True,core=True)
    irc_nick = models.CharField(max_length=100, null=True, blank=True, db_index=True,core=True)
    irc_server = models.CharField(max_length=150, null=True, blank=True, db_index=True,core=True)
    common_channels = models.CharField(max_length=500, null=True, blank=True, db_index=True,core=True)
    user_photo = models.ImageField(upload_to='user_photos',null=True,blank=True,core=True)
    site = models.URLField(db_index=True, blank=True, null=True,core=True)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    def save(self):
        # We use PIL's Image object
        # Docs: http://www.pythonware.com/library/pil/handbook/image.htm
        from PIL import Image
   
        # Set our max image size in a tuple (max width, max height)
        MAX_IMAGE_SIZE = (150, 150)
   
        # Save image so we can get the filename
        # it appears this is no longer necessary
        # self.save_user_photo_file(self.get_user_photo_filename(), '', save=False)
   
        # Open image in order to resize
        if (self.get_user_photo_filename()):
            image = Image.open(self.get_user_photo_filename())
   
            # Convert to RGB if necessary
            # Thanks to Limodou on DjangoSnippets.org
            # http://www.djangosnippets.org/snippets/20/
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
       
            # We use our PIL Image object to resize
            # Additionally, we use Image.ANTIALIAS to make the image look better.
            # Without antialiasing the image pattern artifacts may result.
            image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
     
            # Save the thumbnail
            try:
                image.save(self.get_user_photo_filename())
            except KeyError:
                pass
            # Save this photo instance
        super(UserProfile, self).save()

    class Admin:
        search_fields = ['job_title','common_channels','@bio','site']
        list_display = ('user', 'irc_nick', 'common_channels')
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

class PostTag(models.Model):
    name = models.CharField(max_length=150,db_index=True)
    created = models.DateTimeField()

    class Admin:
        pass

class LinkItems(models.Model):
    href = models.CharField(max_length=200)
    innertext = models.CharField(max_length=100)
    order = models.IntegerField()

    class Admin:
        search_fields = ['innertext']
        list_filter = ['href', 'innertext']
        list_display = ('order', 'href', 'innertext')

    class Meta:
        verbose_name_plural = "Link Items"

class PostFiles(models.Model):
    display_name = models.CharField(max_length=300,db_index=True)
    upload_date = models.DateTimeField(db_index=True)
    uploader = models.ForeignKey(User)
    posts = models.ManyToManyField('BlogPost')
    file = models.FileField(upload_to="post_files")

    class Admin:
        pass

    class Meta:
        verbose_name_plural = "Post Files"

class BlogPost(models.Model): 
    poster = models.ForeignKey(User, core=True)
    created = models.DateTimeField(db_index=True)
    display_date = models.DateTimeField(db_index=True)
    tags = models.ForeignKey(PostTag,edit_inline=True,blank=True,null=True)
    files = models.ManyToManyField(PostFiles,blank=True, null=True)
    content = models.TextField()
    title = models.CharField(max_length=200,db_index=True)

    class Admin:
        search_fields = ['title','@content']
        list_filter = ['poster', 'created','display_date', 'title']
        list_display = ('title', 'poster', 'created', 'display_date')
        fields = (
            (None, {
                'fields': ('poster', 'title', 'content', 'created', 'display_date', 'tags')
                }),
                ('Extra Content', {
                    'classes': 'collapse',
                    'fields': ('files',)
                    }),
                )

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
    uid = models.CharField(max_length=40,null=True,blank=True)
    text = models.CharField(max_length=10,null=True,blank=True)

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
            print "result: " + str(result.answer)
            print "given answer: " + given_answer
        if not result:
            return CAPTCHA_UID_NOT_FOUND
        if result.valid_until<datetime.now():
            result.delete()
            return CAPTCHA_REQUEST_EXPIRED 
        if int(result.answer)!=int(given_answer):
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

from django.contrib.syndication.feeds import Feed

class LatestEntries(Feed):
#    print "Inside LatestEntries"
    title = "Latest News from The Utah Open Source Conference 2008 "
    link = "/"
    description = "Watch this rss feed to keep up on all that's going on prior and during the Utah Open Source Conference 2008.  Feel free to sign up at 2008.utosc.com"

    def items(self):
        return BlogPost.objects.order_by('-display_date')[:10]

    def item_link(self, item):
        return Static.HOST_NAME + '/post/' + str(item.id) + '/'

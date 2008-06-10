from django.db import models
from django.contrib.auth.models import User
from common.models import UserProfile

from voting.models import Vote

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Denied', 'Denied'),
    ('Cancelled', 'Speaker Cancelled'),
    ('Alternate', 'Alternate'),
    ('Approved', 'Approved'),
)

AUDIENCE_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
    ('Tutorial', 'Tutorial'),
)

CATEGORY_CHOICES = (
    ('Business', 'Business'),
    ('Technology', 'Technology'),
    ('Community', 'Community'),
    ('Educational', 'Educational'),
)

# Create your models here.    
class Category(models.Model):
    '''
    >>> c = Category(name="hot_or_not")
    >>> c.name
    'hot_or_not'
    '''
    name = models.CharField(max_length=150,choices=CATEGORY_CHOICES, db_index=True)

    def __unicode__(self):
        return self.name
    
    class Admin:
        list_display = ('name',)
        pass
    
    class Meta:
        verbose_name_plural = "Categories"

class Room(models.Model):
    name = models.CharField(max_length=70)
    # this is for the 'you are here' section on a map.
    # could be coordinates, but I think it'll be an image for now
    here = models.ImageField(upload_to='here',blank=True,null=True)

    def __unicode__(self):
        return self.name
    
    class Admin:

        pass

class Status(models.Model):
    '''
    >>> c = Status(name="hot_or_not")
    >>> c.name
    'hot_or_not'
    '''
    name = models.CharField(max_length=70,choices=STATUS_CHOICES, db_index=True)

    def __unicode__(self):
        return self.name
    
    class Admin:

        pass
    
    class Meta:
        verbose_name_plural = "Statuses"

class AudienceType(models.Model):
    '''
    >>> a = AudienceType(name="Legendary")
    >>> a.name
    'Legendary'
    '''
    name = models.CharField(max_length=150, choices=AUDIENCE_CHOICES, db_index=True)

    def __unicode__(self):
        return self.name
    class Admin:
        pass

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
    audiences = models.ManyToManyField(AudienceType)
    title = models.CharField(max_length=150, db_index=True)
    short_abstract = models.TextField(max_length=5000)
    long_abstract = models.TextField(blank=True,null=True)
    # the default here is a hack, it should really be
    # default=Status('Pending').id or something
    status = models.ForeignKey(Status, default=1)
    slides = models.FileField(upload_to="slides",blank=True,null=True)
    presenter = models.ForeignKey(UserProfile)
    score = models.IntegerField(blank=True, null=True)
    # allows for scheduling of the presentation once its approved
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    location = models.ForeignKey(Room, blank=True, null=True)
    
    def __unicode__(self):
        return self.title

    class Admin:
        list_filter = ['presenter', 'cat', 'audiences','status']
        fields = (
           (None, {
               'fields': ('presenter', 'title', 'short_abstract', 'cat', 'audiences', 'score', 'status')
           }),
           ('Extra Information', {
               'classes': 'collapse',
               'fields' : ('long_abstract', 'slides', 'start', 'end', 'location')
           }),
        )
        list_display = ('presenter', 'title', 'get_score', 'short_abstract', 'status')
        search_fields = ['@longabstract','status','@title','foreign_key__cat']

    @models.permalink
    def get_absolute_url(self):
        return ('speakers.views.show_presentation', [str(self.id)])

    def get_score(self):
        """Returns the aggregate score for this presentation from the
        django-voting app.

        """
        return Vote.objects.get_score(self)['num_votes']
    get_score.short_description = "Voting score"

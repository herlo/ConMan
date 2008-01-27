from django.db import models
from django.contrib.auth.models import User

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
    def __str__(self):
        return self.name
    
    class Admin:
        pass
    
    class Meta:
        verbose_name_plural = "Categories"
    
class VolunteerRole(models.Model):
    '''
    >>> v = VolunteerRole(name = "killa")
    >>> v.name
    'killa'
    '''
    name = models.CharField(max_length=150, db_index=True)
    def __str__(self):
        return self.name
    class Admin:
        pass
    
class AudienceType(models.Model):
    '''
    >>> a = AudienceType(name="Legendary")
    >>> a.name
    'Legendary'
    '''
    name = models.CharField(max_length=150, db_index=True)
    def __str__(self):
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
    def __str__(self):
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
    role = models.ForeignKey(VolunteerRole,related_name='role')
    request = models.ForeignKey(VolunteerRole, related_name='request')
    comments = models.TextField()
    
    def __str__(self):
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
    def __str__(self):
        return " Presentation " + self.pk
    class Admin:
        list_filter = ['cat','audience']
    
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
       ... shirtsize = shirt,
       ... volunteerinfo = vol )
 
       
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
 
     ''' 
    user = models.ForeignKey(User,unique=True)
    bio = models.CharField(max_length=500)
    presentation = models.ForeignKey(Presentation)
    #shirtsize = models.CharField(max_length=200, db_index=True, choices=SHIRT_SIZES)
    shrirtsize = models.ForeignKey(ShirtSize)
    volunteerinfo = models.ForeignKey(Volunteer)
    job_title = models.CharField(max_length=200, db_index=True)
    irc_nick = models.CharField(max_length=100, db_index=True)
    
    def __str__(self):
        return str(self.user)
    
    class Admin:
        pass

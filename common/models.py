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
    Create the VolunteerRole
      >>> VolunteerRole.objects.create(name="Fun Sucker")
      <VolunteerRole: Fun Sucker>

    Create a volunteer with the first default role value
      >>> v = Volunteer.objects.create(
      ... role=VolunteerRole.objects.get(id=1),
      ... request=VolunteerRole.objects.get(id=1),
      ... comments="This is my comment")

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
        return self.role.name + " Volunteer " +self.pk
    class Admin:
        list_filter = ['role','request']
        
class Presentation(models.Model):
    cat = models.ForeignKey(Category)
    audience = models.ForeignKey(AudienceType)
   # audience = models.CharField(max_length=200, choices=AUDIENCE_CHOICES,db_index=True)
    abstract = models.CharField(max_length=500)
    longabstract = models.TextField()
    approved = models.BooleanField()
    
    def __str__(self):
        return " Presentation " + self.pk
    class Admin:
        list_filter = ['cat','audience']
    
class UserProfile(models.Model):
    user = models.ForeignKey(User,unique=True)
    bio = models.CharField(max_length=500)
    presentation = models.ForeignKey(Presentation)
    #shirtsize = models.CharField(max_length=200, db_index=True, choices=SHIRT_SIZES)
    shrirtsize = models.ForeignKey(ShirtSize)
    volunteerinfo = models.ForeignKey(Volunteer)

    def __str__(self):
        return str(self.user)
    
    class Admin:
        pass

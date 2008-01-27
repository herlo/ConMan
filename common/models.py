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
    name = models.CharField(max_length=150,db_index=True)
    def __str__(self):
        return self.name
    
    class Admin:
        pass

    
class VolunteerRole(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    def __str__(self):
        return self.name
    class Admin:
        pass
    
class AudienceType(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    def __str__(self):
        return self.name
    class Admin:
        pass
    
class ShirtSize(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    def __str__(self):
        return self.name
    class Admin:
        pass
    
class Volunteer(models.Model):
    #role = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    #request = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    role = models.ForeignKey(VolunteerRole,related_name='role')
    request = models.ForeignKey(VolunteerRole, related_name='request')
    comments = models.TextField()
    
    class Admin:
        list_filter = ['role','request']
        
class Presentation(models.Model):
    cat = models.ForeignKey(Category)
    audience = models.ForeignKey(AudienceType)
   # audience = models.CharField(max_length=200, choices=AUDIENCE_CHOICES,db_index=True)
    abstract = models.CharField(max_length=500)
    longabstract = models.TextField()
    class Admin:
        list_filter = ['cat','audience']
    
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    bio = models.CharField(max_length=500)
    presentation = models.ForeignKey(Presentation)
    #shirtsize = models.CharField(max_length=200, db_index=True, choices=SHIRT_SIZES)
    shrirtsize = models.ForeignKey(ShirtSize)
    volunteerinfo = models.ForeignKey(Volunteer)
    
    class Admin:
        pass
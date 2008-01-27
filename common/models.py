from django.db import models
from django.contrib.auth.models import User

AUDIENCE_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

VOLUNTEER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

SHIRT_SIZES = (
    ('S', 'Small'),
    ('XS', 'Xtra-Small'),
)
# Create your models here.    
class Catagory(models.Model):
    name = models.CharField(max_length=150,db_index=True)

#class AudienceType(models.Model):
    #name = models.CharField(max_length=150)
    
class Volunteer(models.Model):
    role = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    request = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    comments = models.TextField()
    
#class VolunteerRoles(models.Model):
    #name = models.CharField(max_length=150)
    
class Presentation(models.Model):
    cat = models.ForeignKey(Catagory)
    audience = models.CharField(max_length=200, choices=AUDIENCE_CHOICES,db_index=True)
    shortsummary = models.CharField(max_length=500)
    longsummary = models.TextField()
    
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    bio = models.CharField(max_length=500)
    presentation = models.ForeignKey(Presentation)
    shirtsize = models.CharField(max_length=200, db_index=True, choices=SHIRT_SIZES)
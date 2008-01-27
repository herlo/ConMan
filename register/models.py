from django.db import models
AUDIENCE_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

VOLUNTEER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    bio = models.CharField(max_length=500)
    presentation = models.ForeignKey(Presentation)
    
    
class Presentation(models.Model):
    cat = models.ForeignKey(Catagory)
    audience = models.CharField(max_length=200, choices=AUDIENCE_CHOICES)
    shortsummary = models.CharField(max_length=500)
    longsummary = models.TextField()
    
    
    
class Catagory(models.Model):
    name = models.CharField(max_length=150)

#class AudienceType(models.Model):
    #name = models.CharField(max_length=150)
    
class Volunteer(models.Model):
    role = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES)
    request = models.CharField(max_lenght=150, choices=VOLUNTEER_CHOICES)
#class VolunteerRoles(models.Model):
    #name = models.CharField(max_length=150)
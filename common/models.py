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

CATEGORY_CHOICES = (
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

class Volunteer(models.Model):
    role = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    request = models.CharField(max_length=150, choices=VOLUNTEER_CHOICES,db_index=True)
    comments = models.TextField()
    
class Presentation(models.Model):
    cat = models.CharField(max_length=200, choices=CATEGORY_CHOICES, db_index=True)
    audience = models.CharField(max_length=200, choices=AUDIENCE_CHOICES,db_index=True)
    shortsummary = models.CharField(max_length=500)
    longsummary = models.TextField()
    
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    bio = models.CharField(max_length=500)
    presentation = models.ForeignKey(Presentation)
    shirtsize = models.CharField(max_length=200, db_index=True, choices=SHIRT_SIZES)

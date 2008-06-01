from django.db import models

# Create your models here.
LEVEL_CHOICES = (
    ('Diamond', 'Diamond'),
    ('Sapphire', 'Sapphire'),
    ('Emerald', 'Emerald'),
    ('General', 'General'),
)

class Level(models.Model):
    name = models.CharField(max_length=150,choices=LEVEL_CHOICES, db_index=True)

class Sponsor(models.Model):
    name = models.ManyToManyField(AudienceType)
    level = models.ForeignKey(Level)
    about = models.TextField()
    logo = models.ImageField(upload_to='sponsor_logo',blank=True,null=True)

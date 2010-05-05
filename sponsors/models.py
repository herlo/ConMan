from django.db import models
import Image
import os

largeImageWidth = 250;
smallImageWidth = 120;

# Create your models here.
LEVEL_CHOICES = (
    ('Diamond', 'Diamond'),
    ('Sapphire', 'Sapphire'),
    ('Emerald', 'Emerald'),
    ('General', 'General'),
)

class Level(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    order = models.IntegerField(default=10)

    def __unicode__(self):
        return self.name

class Sponsor(models.Model):
    company = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    email = models.EmailField(blank=True,null=True)
    url = models.CharField(max_length=250)
    about = models.TextField(blank=True,null=True)
    level = models.ForeignKey(Level,blank=True,null=True)
    sm_logo = models.ImageField(upload_to='img/sponsors')
    lg_logo = models.ImageField(upload_to='img/sponsors')


    def save(self):

        if self.sm_logo:
            newImage = Image.open(self.sm_logo.path)
            newHeight = (smallImageWidth * newImage.size[1])/ newImage.size[0]
            newImage.thumbnail((smallImageWidth,newHeight), Image.ANTIALIAS)
            newImage.save(self.sm_logo.path);

        if self.lg_logo:
            newImage = Image.open(self.lg_logo.path)
            newHeight = (largeImageWidth * newImage.size[1])/ newImage.size[0]
            newImage.thumbnail((largeImageWidth,newHeight), Image.ANTIALIAS)
            newImage.save(self.lg_logo.path);

        super(Sponsor, self).save()

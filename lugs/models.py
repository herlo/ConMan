from django.db import models
import Image
import os

largeImageWidth = 200;
smallImageWidth = 80;

class Type(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    order = models.IntegerField(default=10)

    def __unicode__(self):
        return self.name

#    class Admin:
#        list_display = ('name', 'order')

class LUG(models.Model):
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    email = models.EmailField(blank=True,null=True)
    url = models.CharField(max_length=250)
    about = models.TextField(blank=True,null=True)
    type = models.ForeignKey(Type,blank=True,null=True)
    sm_logo = models.ImageField(upload_to='img/sponsors',blank=True,null=True)
    lg_logo = models.ImageField(upload_to='img/sponsors',blank=True,null=True)

#    class Admin:
#        list_display = ('company', 'contact', 'level')

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

        super(LUG, self).save()

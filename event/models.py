from datetime import datetime
from django.db import models

# Create your models here.
class EventDays(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

class Location(models.Model):
    name = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    primary = models.BooleanField()

class HostOrg(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    contacts = models.ManyToManyField(Contact)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    logo = models.FileField(upload_to='logos')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Location)
    days = models.ForeignKey(EventDays)
    host = models.ForeignKey(HostOrg)

    def __unicode__(self):
        return self.name

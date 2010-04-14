from datetime import datetime
from django.db import models
from django.contrib.sites.models import Site


# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    primary = models.BooleanField()

    def __unicode__(self):
        return self.name

class HostOrg(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    contacts = models.ManyToManyField(Contact)

    def __unicode__(self):
        return self.name

from common.models import Option

class Event(models.Model):
    logo = models.ImageField(upload_to='themes/' + Option.get_theme_name() + '/img/logos')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Location)
    host = models.ForeignKey(HostOrg)
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return self.name

class EventDay(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return str(self.event) + ": " + str(self.date)

from django.db import models

# Create your models here.
class Event(models.Model):
    logo
    name
    summary
    description
    host

class EventDays(models.Model):
    start
    end

class Location(models.Model):
    name
    street1
    street2
    city
    state
    zip

class HostOrg(models.Model):
    name
    url
    contacts

class Contact(models.Model):
    name
    email
    phone
    primary = bool

class Attendee(models.Model):
    first_name
    last_name
    zip_code
    email
    ticket
    user
    meta
class AttendeeMeta(models.Model):
    name
    value

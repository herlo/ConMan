from datetime import datetime
from django.db import models

class Event(models.Model):
    logo = models.FileField(upload_to='logos')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    host = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

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

class TicketType(models.Model):

    name = models.CharField(max_length=10, help_text="Short name (10 characters) of Ticket Type")
    summary = models.TextField(help_text="Short explanation of the ticket (eg. Thursday Only)")

    def __unicode__(self):
        # return self.get_name_display()
        return self.name

class Ticket(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=60, help_text="Complete (long) description of the ticket")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price before discount")
    type = models.ManyToManyField(TicketType, help_text="Used for tracking types of attendees (Expo vs Full)")
    active = models.BooleanField(default=True, help_text="Does this show up on the main site?")
    start_date = models.DateTimeField(blank=True, null=True, help_text="Ticket will be available at this date and time")
    end_date = models.DateTimeField(blank=True, null=True, help_text="Ticket will be be removed at this date and time")
    event = models.ForeignKey(Event)

    def __unicode__(self):
        # return self.get_name_display()
        return self.name

class ItemOption(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class Item(models.Model):

    name = models.CharField(max_length=50)
    summary = models.TextField(help_text="Short explanaion of the item (eg. Conference T-Shirt)")
    description = models.TextField(max_length=60, help_text="Complete (long) description of the item")
    active = models.BooleanField(default=True, help_text="Does this show up on the main site?")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price before discounts")
    event = models.ForeignKey(Event)
    tickets = models.ManyToManyField(Ticket)
    options = models.ManyToManyField(ItemOption)

    def __unicode__(self):
        return self.get_name_display()

DISCOUNT_CHOICES = (
  ('%', 'Percent discount'),
  ('$', 'Dollar discount'),
)

class Discount(models.Model):

    name = models.CharField(max_length=10, help_text="Code given to customer")
    description = models.CharField(max_length="60", help_text="What is this discount used for?")
    tickets = models.ForeignKey(Ticket, blank=True, null=True, help_text="Ticket(s) which this discount applies")
    items = models.ForeignKey(Item, blank=True, null=True, help_text="Item(s) which this discount applies")
    modifier = models.CharField(max_length="1", choices=DISCOUNT_CHOICES, help_text="Modify price by percent (%) or dollars ($), price will not go below $0 total when discount is applied")
    amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="Amount removed from ticket price")
    count = models.IntegerField(max_length=4, default=0, help_text="Total number of discounts available. Zero (0) is unlimited")
    active = models.BooleanField(default=True, help_text="Does this show up on the main site?")
    start_date = models.DateTimeField(blank=True, null=True, help_text="Ticket will be available at this date and time")
    end_date = models.DateTimeField(blank=True, null=True, help_text="Ticket will be be removed at this date and time")

    def __unicode__(self):
        return self.get_name_display()


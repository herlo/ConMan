from django.contrib import admin
from django.contrib.sites.models import Site
from ticketing.models import TicketType,Ticket,Discount,Item

site = admin.AdminSite()

admin.site.register(Item)
admin.site.register(Discount)
admin.site.register(Ticket)
admin.site.register(TicketType)

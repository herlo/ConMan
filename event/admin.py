from django.contrib import admin
from django.contrib.sites.models import Site
from event.models import Event,Location,Contact,HostOrg,EventDay

#events
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Contact)
admin.site.register(HostOrg)
admin.site.register(EventDay)

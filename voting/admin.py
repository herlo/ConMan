from django.contrib import admin
from django.contrib.sites.models import Site
from voting.models import Vote

site = admin.AdminSite()

admin.site.register(Vote)

from django.contrib import admin
from speakers.models import Category,Room,Status,AudienceType,Presentation
from common.models import ShirtSize, UserProfile



admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Status)
admin.site.register(AudienceType)
admin.site.register(Presentation)

admin.site.register(ShirtSize)
admin.site.register(UserProfile)

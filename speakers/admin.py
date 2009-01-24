from django.contrib import admin
from django.contrib.sites.models import Site
from speakers.models import Category,Room,Status,AudienceType,Presentation

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    class Meta:
        verbose_name_plural = "Categories"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Room)
admin.site.register(Status)
admin.site.register(AudienceType)

class PresentationAdmin(admin.ModelAdmin):
    list_filter = ('presenter', 'cat', 'audiences','status')
    list_display = ('title', 'presenter', 'get_score', 'short_abstract', 'status')
    search_fields = ('@longabstract','status','@title','foreign_key__cat')


admin.site.register(Presentation, PresentationAdmin)

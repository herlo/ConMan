from django import template
from django.contrib.flatpages.models import FlatPage

register = template.Library()

def show_flatpages():
    flatpages = FlatPage.objects.all().order_by('id')
    return {'flatpages': flatpages}

# register tags 	
 
register.inclusion_tag('flatpage_links.html')(show_flatpages)


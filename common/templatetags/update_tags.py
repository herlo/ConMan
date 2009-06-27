from django import template
from updates.models import Update

register = template.Library()

def latest_update():
    update = Update.objects.order_by('updated')[0]
    return {'update': update}

# register tags 	
 
register.inclusion_tag('latest_update.html')(latest_update)


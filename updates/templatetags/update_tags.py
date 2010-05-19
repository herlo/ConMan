from django import template
from updates.models import Update
from django.contrib.auth.models import User

register = template.Library()

def latest_update():
    try:
        items = Update.objects.all().order_by('-updated')
        update = items[0]
    except:
        items = Update(name="Nothing Yet", description="You haven't entered any data here. Add something in the admin",
                author=User.objects.get(username='conman'))
        update = items
    return {'update': update}

# register tags

register.inclusion_tag('updates/latest_update.html')(latest_update)


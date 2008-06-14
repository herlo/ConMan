from django import template
from sponsors.models import Sponsor, Level

register = template.Library()

def show_sponsors():
    sponsors = Sponsor.objects.all().order_by('-level__order')
    return {'sponsors': sponsors}

# register tags 	
 
register.inclusion_tag('rightmenu.html')(show_sponsors)


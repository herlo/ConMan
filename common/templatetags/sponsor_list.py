from django import template
from sponsors.models import Sponsor, Level
import random

register = template.Library()

def show_sponsors():
    sponsors = Sponsor.objects.all().order_by('-level__order')
    return {'sponsors': sponsors}

def random_sponsor():
    count = Sponsor.objects.count()
    
    random_id = random.randrange(1, count)
    print "Random ID: " + str(random_id)

    sponsor = Sponsor.objects.get(id=random_id)
    return {'sponsor': sponsor}


# register tags 	
 
register.inclusion_tag('rightmenu.html')(show_sponsors)
register.inclusion_tag('randomsponsor.html')(random_sponsor)


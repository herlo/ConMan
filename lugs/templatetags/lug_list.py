from django import template
from lugs.models import LUG, Type

register = template.Library()

def show_lugs():
    lugs = LUG.objects.all().order_by('-type__order')
    return {'lugs': lugs}

# register tags

register.inclusion_tag('leftmenu.html')(show_lugs)


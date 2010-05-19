from django import template
from django.contrib.sites.models import Site
from common.models import Theme,Option

register = template.Library()

def theme():
    """
    Returns the "template_name".
    """

    current_site = Site.objects.get_current()

    try:
        option = Option.objects.get(site=current_site)
        template_theme = unicode(option.theme.name)
    except:
        template_theme = u'default'

    return template_theme

register.simple_tag(theme)


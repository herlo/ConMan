from django import template
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter
from speakers.models import Presentation
from common.models import UserProfile

register = template.Library()

def get_presenters(pres_id):

    presentations = Presentation.objects.get(id=pres_id)
    presenters = presentations.presenter.all()

    print "presenters: " + str(presenters)

    pres_list = list()
    count = 0
    spkr_count = 0
    for p in presenters:
        full_name = p.user.get_full_name()
        pres_list.append({"uid": str(p.user.id), "name": full_name})
        spkr_count += 1

    ret_txt = ""
    for pd in pres_list:
        count += 1
        ret_txt += "<a href=\"/speaker/" + pd['uid'] + "/\">" + pd['name'] + "</a>"
        if spkr_count > count:
            ret_txt += ", "

    return ret_txt

# register tags

register.filter('get_presenters', get_presenters)


from updates.models import Update
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.

def history(request):
    items = Update.objects.all().order_by('-updated')
    page_info = { 'title': 'Updates', 'item_name_heading': 'Title', 'item_value_heading': 'Description', 'updated_heading': 'When' }

    return render_to_response('generic_list.html', {'items': items, 'page_info': page_info }, context_instance=RequestContext(request))

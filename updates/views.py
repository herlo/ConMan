from updates.models import Update
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
import urllib
import simplejson as json
import time
import sys

def twitter(request):
    
    if request.method == 'GET':
        return render_to_response('show_update_tracker.html', {}, context_instance=RequestContext(request))

    if request.method == 'POST':

        url = 'http://search.twitter.com/search.json?q=utosc%20OR%20%23utosc2009%20OR%20%23utosc&since_id='+ request.POST['since']
        
        tweets = urllib.urlopen(url).read()
        
        return render_to_response('show_twitter_json.html', {'tweets':tweets}, context_instance=RequestContext(request))

def history(request):
    items = Update.objects.all().order_by('-updated')

    page_info = { 'title': 'Updates', 'item_name_heading': 'Title', 'item_value_heading': 'Description', 'updated_heading': 'When' }

    return render_to_response('generic_list.html', {'items': items, 'page_info': page_info }, context_instance=RequestContext(request))

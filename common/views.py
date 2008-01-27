# Create your views here.
from django.shortcuts import render_to_response
from common.models import User,UserProfile,Presentation,Category


def test(request):
    
    return render_to_response('test_template.html',None)


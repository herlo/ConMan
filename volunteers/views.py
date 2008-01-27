# Create your views here.
from conman.common.models import Volunteer, UserProfile

def index(request, ):
    try:
        v = Volunteer.objects.create(
	vp = User.objects.get_profile(pk=user_id)
    except User.DoesNotExist:
        raise Http404
    return render_to_response('volunteers.html')

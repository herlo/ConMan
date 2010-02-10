from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create your models here.
class VolunteerRole(models.Model):
    '''
    >>> v = VolunteerRole(name = "killa")
    >>> v.name
    'killa'
    '''
    name = models.CharField(max_length=150, db_index=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "Volunteer Role"
        verbose_name_plural = "Volunteer Roles"


class Volunteer(models.Model):
    """
    A registrant may wish to volunteer to help with the conference.  This
    objects represents a user who has signed up to volunteer.  A User object
    is required to have an accompanying UserProfile object to have a
    Volunteer object associated with it.  This should be the case for user's
    registered through the normal site registration.

    Create a User
    >>> u = User.objects.create(username='testuser', first_name='Test',
    ...                         last_name='User', password="utos")

    Create a UserProfile attached to the user
    >>> p = UserProfile.objects.create(user=User.objects.get(id=u.id))

    Create a VolunteerRole for the user
    >>> vr = VolunteerRole.objects.get(name="Room Manager")
    >>> vr
    <VolunteerRole: Room Manager>

    Create a volunteer with the first default role value
    >>> v = Volunteer.objects.create(
    ... role=VolunteerRole.objects.get(id=vr.id),
    ... requested=VolunteerRole.objects.get(id=vr.id),
    ... comments="This is my comment",
    ... volunteer=UserProfile.objects.get(id=u.id))
    >>> v
    <Volunteer: Test User>
    >>> v.role
    <VolunteerRole: Room Manager>
    >>> v.requested
    <VolunteerRole: Room Manager>
    >>> v.comments
    'This is my comment'
    """
    role = models.ForeignKey(VolunteerRole, related_name='role', blank=True,
                             null=True)
    requested = models.ForeignKey(VolunteerRole, related_name='requested')
    comments = models.TextField()
    volunteer = models.ForeignKey(UserProfile, unique=True)

    def __unicode__(self):
        role = "(" + self.requested.name + ")"
        if self.role is not None:
            role = " -- " + self.role.name
        return self.volunteer.user.get_full_name()
    class Meta:
        permissions = (
            ("can_drive", "Can drive"),
            ("can_vote", "Can vote in elections"),
            ("can_drink", "Can drink alcohol"),
        )
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"

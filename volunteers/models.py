from django.db import models
from django.contrib.auth.models import User
from common.models import UserProfile

# Create your models here.
VOLUNTEER_CHOICES = (
    ('RMGR', 'Room Manager'),
    ('USH', 'Usher'),
    ('GRT', 'Greeter'),
    ('HRT', 'Heartsbane'),   # Kevin WTH is this?
    ('TEK', 'Technician'),
)

class VolunteerRole(models.Model):
    '''
    >>> v = VolunteerRole(name = "killa")
    >>> v.name
    'killa'
    '''
    name = models.CharField(max_length=150, db_index=True)
    def __unicode__(self):
        return self.name
    class Admin:
        pass

class Volunteer(models.Model):
    '''
    Create a VolunteerRole for the user
      >>> VolunteerRole.objects.create(name="Fun Sucker")
      <VolunteerRole: Fun Sucker>

    Create a volunteer with the first default role value
      >>> v = Volunteer.objects.create(
      ... role=VolunteerRole.objects.get(id=1),
      ... request=VolunteerRole.objects.get(id=1),
      ... comments="This is my comment")

      >>> v
      <Volunteer: Fun Sucker Volunteer 2>
      >>> v.role
      <VolunteerRole: Fun Sucker>
      >>> v.request
      <VolunteerRole: Fun Sucker>
      >>> v.comments
      'This is my comment'
    '''
    role = models.ForeignKey(VolunteerRole,related_name='role',blank=True, null=True)
    request = models.ForeignKey(VolunteerRole, related_name='request')
    comments = models.TextField()
    volunteer = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.role.name + " Volunteer " + str(self.pk)
    class Admin:
        list_filter = ['role','request']
        search_fields = ['@comments']



from south.db import db
from django.db import models
from volunteers.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VolunteerRole'
        db.create_table('volunteers_volunteerrole', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=150, db_index=True)),
        ))
        db.send_create_signal('volunteers', ['VolunteerRole'])
        
        # Adding model 'Volunteer'
        db.create_table('volunteers_volunteer', (
            ('requested', models.ForeignKey(orm.VolunteerRole, related_name='requested')),
            ('role', models.ForeignKey(orm.VolunteerRole, related_name='role', null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('comments', models.TextField()),
            ('volunteer', models.ForeignKey(orm['common.UserProfile'], unique=True)),
        ))
        db.send_create_signal('volunteers', ['Volunteer'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VolunteerRole'
        db.delete_table('volunteers_volunteerrole')
        
        # Deleting model 'Volunteer'
        db.delete_table('volunteers_volunteer')
        
    
    
    models = {
        'volunteers.volunteerrole': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'common.userprofile': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'volunteers.volunteer': {
            'Meta': {'permissions': '(("can_drive","Can drive"),("can_vote","Can vote in elections"),("can_drink","Can drink alcohol"),)'},
            'comments': ('models.TextField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'requested': ('models.ForeignKey', ['VolunteerRole'], {'related_name': "'requested'"}),
            'role': ('models.ForeignKey', ['VolunteerRole'], {'related_name': "'role'", 'null': 'True', 'blank': 'True'}),
            'volunteer': ('models.ForeignKey', ['UserProfile'], {'unique': 'True'})
        }
    }
    
    complete_apps = ['volunteers']

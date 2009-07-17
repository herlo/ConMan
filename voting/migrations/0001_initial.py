
from south.db import db
from django.db import models
from voting.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Vote'
        db.create_table('votes', (
            ('object_id', models.PositiveIntegerField()),
            ('vote', models.SmallIntegerField()),
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'])),
            ('user', models.ForeignKey(orm['auth.User'])),
        ))
        db.send_create_signal('voting', ['Vote'])
        
        # Creating unique_together for [user, content_type, object_id] on Vote.
        db.create_unique('votes', ['user_id', 'content_type_id', 'object_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Vote'
        db.delete_table('votes')
        
        # Deleting unique_together for [user, content_type, object_id] on Vote.
        db.delete_unique('votes', ['user_id', 'content_type_id', 'object_id'])
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'voting.vote': {
            'Meta': {'unique_together': "(('user','content_type','object_id'),)", 'db_table': "'votes'"},
            'content_type': ('models.ForeignKey', ['ContentType'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.PositiveIntegerField', [], {}),
            'user': ('models.ForeignKey', ['User'], {}),
            'vote': ('models.SmallIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['voting']

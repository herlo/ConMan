
from south.db import db
from django.db import models
from updates.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Update'
        db.create_table('updates_update', (
            ('updated', models.DateTimeField(editable=False)),
            ('description', models.TextField(max_length=140, null=True, blank=True)),
            ('author', models.ForeignKey(orm['auth.User'])),
            ('created', models.DateTimeField(editable=False)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=150, db_index=True)),
        ))
        db.send_create_signal('updates', ['Update'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Update'
        db.delete_table('updates_update')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'updates.update': {
            'author': ('models.ForeignKey', ['User'], {}),
            'created': ('models.DateTimeField', [], {'editable': 'False'}),
            'description': ('models.TextField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'updated': ('models.DateTimeField', [], {'editable': 'False'})
        }
    }
    
    complete_apps = ['updates']


from south.db import db
from django.db import models
from updates.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Update.link_title'
        db.add_column('updates_update', 'link_title', models.CharField(max_length=25, null=True, blank=True))

        # Adding field 'Update.link_url'
        db.add_column('updates_update', 'link_url', models.CharField(max_length=150, null=True, blank=True))

        # Adding field 'Update.social_info'
        db.add_column('updates_update', 'social_info', models.CharField(max_length=140, null=True, blank=True))

        # Changing field 'Update.description'
        db.alter_column('updates_update', 'description', models.TextField(max_length=500, null=True, blank=True))



    def backwards(self, orm):

        # Deleting field 'Update.link_title'
        db.delete_column('updates_update', 'link_title')

        # Deleting field 'Update.link_url'
        db.delete_column('updates_update', 'link_url')

        # Deleting field 'Update.social_info'
        db.delete_column('updates_update', 'social_info')

        # Changing field 'Update.description'
        db.alter_column('updates_update', 'description', models.TextField(max_length=140, null=True, blank=True))



    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'updates.update': {
            'author': ('models.ForeignKey', ['User'], {}),
            'created': ('models.DateTimeField', [], {'editable': 'False'}),
            'description': ('models.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'link_title': ('models.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'link_url': ('models.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'social_info': ('models.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'updated': ('models.DateTimeField', [], {'editable': 'False'})
        }
    }

    complete_apps = ['updates']

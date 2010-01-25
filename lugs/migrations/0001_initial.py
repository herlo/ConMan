
from south.db import db
from django.db import models
from lugs.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'LUG'
        db.create_table('lugs_lug', (
            ('about', models.TextField(null=True, blank=True)),
            ('name', models.CharField(max_length=150)),
            ('sm_logo', models.ImageField(null=True, upload_to='img/groups', blank=True)),
            ('url', models.CharField(max_length=250)),
            ('id', models.AutoField(primary_key=True)),
            ('lg_logo', models.ImageField(null=True, upload_to='img/groups', blank=True)),
            ('contact', models.CharField(max_length=150)),
            ('type', models.ForeignKey(orm.Type, null=True, blank=True)),
            ('email', models.EmailField(null=True, blank=True)),
        ))
        db.send_create_signal('lugs', ['LUG'])

        # Adding model 'Type'
        db.create_table('lugs_type', (
            ('order', models.IntegerField(default=10)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=150, db_index=True)),
        ))
        db.send_create_signal('lugs', ['Type'])



    def backwards(self, orm):

        # Deleting model 'LUG'
        db.delete_table('lugs_lug')

        # Deleting model 'Type'
        db.delete_table('lugs_type')



    models = {
        'lugs.lug': {
            'about': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('models.CharField', [], {'max_length': '150'}),
            'email': ('models.EmailField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'lg_logo': ('models.ImageField', [], {'null': 'True', 'upload_to': "'img/groups'", 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150'}),
            'sm_logo': ('models.ImageField', [], {'null': 'True', 'upload_to': "'img/groups'", 'blank': 'True'}),
            'type': ('models.ForeignKey', ['Type'], {'null': 'True', 'blank': 'True'}),
            'url': ('models.CharField', [], {'max_length': '250'})
        },
        'lugs.type': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'order': ('models.IntegerField', [], {'default': '10'})
        }
    }

    complete_apps = ['lugs']


from south.db import db
from django.db import models
from common.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ShirtSize'
        db.create_table('common_shirtsize', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
        ))
        db.send_create_signal('common', ['ShirtSize'])
        
        # Adding model 'UserProfile'
        db.create_table('common_userprofile', (
            ('bio', models.TextField(null=True, blank=True)),
            ('user_photo', models.ImageField(storage=OverwriteStorage(), null=True, upload_to=normalize_photo_name, blank=True)),
            ('common_channels', models.CharField(db_index=True, max_length=500, null=True, blank=True)),
            ('company', models.CharField(db_index=True, max_length=200, null=True, blank=True)),
            ('site', models.URLField(blank=True, null=True, db_index=True)),
            ('irc_nick', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
            ('user', models.ForeignKey(orm['auth.User'], unique=True)),
            ('shirt_size', models.ForeignKey(orm.ShirtSize, null=True, blank=True)),
            ('irc_server', models.CharField(db_index=True, max_length=150, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('job_title', models.CharField(db_index=True, max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['UserProfile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ShirtSize'
        db.delete_table('common_shirtsize')
        
        # Deleting model 'UserProfile'
        db.delete_table('common_userprofile')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'common.shirtsize': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'})
        },
        'common.userprofile': {
            'bio': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'common_channels': ('models.CharField', [], {'db_index': 'True', 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'company': ('models.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'irc_nick': ('models.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'irc_server': ('models.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'job_title': ('models.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'shirt_size': ('models.ForeignKey', ['ShirtSize'], {'null': 'True', 'blank': 'True'}),
            'site': ('models.URLField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True'}),
            'user': ('models.ForeignKey', ['User'], {'unique': 'True'}),
            'user_photo': ('models.ImageField', [], {'storage': 'OverwriteStorage()', 'null': 'True', 'upload_to': 'normalize_photo_name', 'blank': 'True'})
        }
    }
    
    complete_apps = ['common']

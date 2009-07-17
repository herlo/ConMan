
from south.db import db
from django.db import models
from speakers.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('speakers_category', (
            ('description', models.TextField(max_length=1000, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=150, db_index=True)),
        ))
        db.send_create_signal('speakers', ['Category'])
        
        # Adding model 'AudienceType'
        db.create_table('speakers_audiencetype', (
            ('description', models.TextField(max_length=1000, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=150, db_index=True)),
        ))
        db.send_create_signal('speakers', ['AudienceType'])
        
        # Adding model 'Room'
        db.create_table('speakers_room', (
            ('id', models.AutoField(primary_key=True)),
            ('here', models.ImageField(null=True, upload_to='here', blank=True)),
            ('name', models.CharField(max_length=70)),
        ))
        db.send_create_signal('speakers', ['Room'])
        
        # Adding model 'Presentation'
        db.create_table('speakers_presentation', (
            ('status', models.ForeignKey(orm.Status, default=get_status)),
            ('short_abstract', models.TextField(max_length=5000)),
            ('end', models.DateTimeField(null=True, blank=True)),
            ('title', models.CharField(max_length=150, db_index=True)),
            ('start', models.DateTimeField(null=True, blank=True)),
            ('cat', models.ForeignKey(orm.Category, blank=True)),
            ('slides', models.FileField(null=True, upload_to="slides", blank=True)),
            ('presenter', models.ForeignKey(orm['common.UserProfile'])),
            ('score', models.IntegerField(null=True, blank=True)),
            ('location', models.ForeignKey(orm.Room, null=True, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('long_abstract', models.TextField(null=True, blank=True)),
        ))
        db.send_create_signal('speakers', ['Presentation'])
        
        # Adding model 'Status'
        db.create_table('speakers_status', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(db_index=True, max_length=70)),
        ))
        db.send_create_signal('speakers', ['Status'])
        
        # Adding ManyToManyField 'Presentation.audiences'
        db.create_table('speakers_presentation_audiences', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('presentation', models.ForeignKey(Presentation, null=False)),
            ('audiencetype', models.ForeignKey(AudienceType, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('speakers_category')
        
        # Deleting model 'AudienceType'
        db.delete_table('speakers_audiencetype')
        
        # Deleting model 'Room'
        db.delete_table('speakers_room')
        
        # Deleting model 'Presentation'
        db.delete_table('speakers_presentation')
        
        # Deleting model 'Status'
        db.delete_table('speakers_status')
        
        # Dropping ManyToManyField 'Presentation.audiences'
        db.delete_table('speakers_presentation_audiences')
        
    
    
    models = {
        'speakers.category': {
            'description': ('models.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'speakers.presentation': {
            'audiences': ('models.ManyToManyField', ['AudienceType'], {}),
            'cat': ('models.ForeignKey', ['Category'], {'blank': 'True'}),
            'end': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location': ('models.ForeignKey', ['Room'], {'null': 'True', 'blank': 'True'}),
            'long_abstract': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'presenter': ('models.ForeignKey', ['UserProfile'], {}),
            'score': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_abstract': ('models.TextField', [], {'max_length': '5000'}),
            'slides': ('models.FileField', [], {'null': 'True', 'upload_to': '"slides"', 'blank': 'True'}),
            'start': ('models.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('models.ForeignKey', ['Status'], {'default': 'get_status'}),
            'title': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'common.userprofile': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'speakers.status': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'db_index': 'True', 'max_length': '70'})
        },
        'speakers.room': {
            'here': ('models.ImageField', [], {'null': 'True', 'upload_to': "'here'", 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '70'})
        },
        'speakers.audiencetype': {
            'description': ('models.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['speakers']

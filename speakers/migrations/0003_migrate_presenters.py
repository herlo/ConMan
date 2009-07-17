
from south.db import db
from django.db import models
from speakers.models import *

class Migration:
    
    no_dry_run = True

    def forwards(self, orm):
        for p in orm.Presentation.objects.values('id', 'presenter'):
            print "Presentation data: " + str(p)
            db.execute("insert into speakers_presentation_presenter (presentation_id, userprofile_id) values(%s, %s)", 
                    [int(p['id']), int(p['presenter'])] )
    
    
    def backwards(self, orm):
        pass
    
    
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

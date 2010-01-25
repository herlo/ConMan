
from south.db import db
from django.db import models
from sponsors.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'Sponsor'
        db.create_table('sponsors_sponsor', (
            ('about', models.TextField(null=True, blank=True)),
            ('sm_logo', models.ImageField(upload_to='img/sponsors')),
            ('level', models.ForeignKey(orm.Level, null=True, blank=True)),
            ('url', models.CharField(max_length=250)),
            ('company', models.CharField(max_length=150)),
            ('email', models.EmailField(null=True, blank=True)),
            ('lg_logo', models.ImageField(upload_to='img/sponsors')),
            ('contact', models.CharField(max_length=150)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('sponsors', ['Sponsor'])

        # Adding model 'Level'
        db.create_table('sponsors_level', (
            ('order', models.IntegerField(default=10)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=150, db_index=True)),
        ))
        db.send_create_signal('sponsors', ['Level'])



    def backwards(self, orm):

        # Deleting model 'Sponsor'
        db.delete_table('sponsors_sponsor')

        # Deleting model 'Level'
        db.delete_table('sponsors_level')



    models = {
        'sponsors.sponsor': {
            'about': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('models.CharField', [], {'max_length': '150'}),
            'contact': ('models.CharField', [], {'max_length': '150'}),
            'email': ('models.EmailField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'level': ('models.ForeignKey', ['Level'], {'null': 'True', 'blank': 'True'}),
            'lg_logo': ('models.ImageField', [], {'upload_to': "'img/sponsors'"}),
            'sm_logo': ('models.ImageField', [], {'upload_to': "'img/sponsors'"}),
            'url': ('models.CharField', [], {'max_length': '250'})
        },
        'sponsors.level': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'order': ('models.IntegerField', [], {'default': '10'})
        }
    }

    complete_apps = ['sponsors']

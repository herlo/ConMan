
from south.db import db
from django.db import models
from speakers.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'Status'
        db.create_table('speakers_status', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(db_index=True, max_length=70)),
        ))
        db.send_create_signal('speakers', ['Status'])
        db.execute("insert into speakers_status (name) values('Pending')")

    def backwards(self, orm):

        # Deleting model 'Status'
        db.delete_table('speakers_status')


    models = {
        'speakers.status': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'db_index': 'True', 'max_length': '70'})
        }
    }

    complete_apps = ['speakers']

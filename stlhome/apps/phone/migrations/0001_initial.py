# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Call'
        db.create_table('phone_call', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sid', self.gf('django.db.models.fields.CharField')(max_length=34)),
            ('bed_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('phone', ['Call'])


    def backwards(self, orm):
        # Deleting model 'Call'
        db.delete_table('phone_call')


    models = {
        'phone.call': {
            'Meta': {'object_name': 'Call'},
            'bed_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '34'})
        }
    }

    complete_apps = ['phone']
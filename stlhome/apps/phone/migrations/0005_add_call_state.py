# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Call.call_state'
        db.add_column('phone_call', 'call_state',
                      self.gf('django_fsm.db.fields.fsmfield.FSMField')(default='welcome', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Call.call_state'
        db.delete_column('phone_call', 'call_state')


    models = {
        'phone.call': {
            'Meta': {'object_name': 'Call'},
            'bed_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'call_state': ('django_fsm.db.fields.fsmfield.FSMField', [], {'default': "'welcome'", 'max_length': '50'}),
            'client_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'shelter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shelters.Shelter']", 'null': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'shelters.shelter': {
            'Meta': {'object_name': 'Shelter'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'classifier_action': ('django.db.models.fields.CharField', [], {'default': "'block'", 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['phone']
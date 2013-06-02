# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shelter'
        db.create_table(u'shelters_shelter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('classifier_action', self.gf('django.db.models.fields.CharField')(default='block', max_length=5)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=13, decimal_places=10, blank=True)),
        ))
        db.send_create_signal(u'shelters', ['Shelter'])

        # Adding model 'Availability'
        db.create_table(u'shelters_availability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shelter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shelters.Shelter'])),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('available', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'shelters', ['Availability'])


    def backwards(self, orm):
        # Deleting model 'Shelter'
        db.delete_table(u'shelters_shelter')

        # Deleting model 'Availability'
        db.delete_table(u'shelters_availability')


    models = {
        u'shelters.availability': {
            'Meta': {'object_name': 'Availability'},
            'available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shelter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shelters.Shelter']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'shelters.shelter': {
            'Meta': {'object_name': 'Shelter'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'classifier_action': ('django.db.models.fields.CharField', [], {'default': "'block'", 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '13', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['shelters']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

import logging
logger = logging.getLogger(__name__)


class Migration(SchemaMigration):

    extensions = ['btree_gist', 'cube', 'earthdistance']

    def forwards(self, orm):
        for extension in self.extensions:
            db.execute('CREATE EXTENSION IF NOT EXISTS %s' % extension)

        db.execute('CREATE INDEX shelters_shelter_geo ON shelters_shelter USING gist (ll_to_earth(latitude, longitude))')

    def backwards(self, orm):
        logger.warning(
            'Not dropping extensions "%s" because I cannot guarantee this is the only app dependent on them' % ', '.join(self.extensions)
        )

        db.execute('DROP INDEX shelters_shelter_geo')

    models = {
        'shelters.availability': {
            'Meta': {'object_name': 'Availability'},
            'available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shelter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shelters.Shelter']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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

    complete_apps = ['shelters']

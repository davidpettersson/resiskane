# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Station'
        db.create_table('skotte_station', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')()),
            ('y', self.gf('django.db.models.fields.IntegerField')()),
            ('metaphone', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('refreshed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('skotte', ['Station'])

    def backwards(self, orm):
        # Deleting model 'Station'
        db.delete_table('skotte_station')

    models = {
        'skotte.station': {
            'Meta': {'object_name': 'Station'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'metaphone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'refreshed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['skotte']
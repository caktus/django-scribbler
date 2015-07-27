# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Scribble'
        db.create_table('scribbler_scribble', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default=u'', max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
        ))
        db.send_create_signal('scribbler', ['Scribble'])


    def backwards(self, orm):
        # Deleting model 'Scribble'
        db.delete_table('scribbler_scribble')


    models = {
        'scribbler.scribble': {
            'Meta': {'object_name': 'Scribble'},
            'content': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['scribbler']
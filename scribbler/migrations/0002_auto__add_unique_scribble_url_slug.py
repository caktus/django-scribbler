# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Scribble', fields ['url', 'slug']
        db.create_unique('scribbler_scribble', ['url', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Scribble', fields ['url', 'slug']
        db.delete_unique('scribbler_scribble', ['url', 'slug'])


    models = {
        'scribbler.scribble': {
            'Meta': {'unique_together': "((u'slug', u'url'),)", 'object_name': 'Scribble'},
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
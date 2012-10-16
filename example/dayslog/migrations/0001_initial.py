# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DaysLog'
        db.create_table(u'dayslog_dayslog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('happenings', self.gf('django.db.models.fields.TextField')(default='<h1>Things that happened today</h1>\n<ol>\n  <li>Clock ticked over midnight.</li>\n</ol>')),
        ))
        db.send_create_signal(u'dayslog', ['DaysLog'])


    def backwards(self, orm):
        # Deleting model 'DaysLog'
        db.delete_table(u'dayslog_dayslog')


    models = {
        u'dayslog.dayslog': {
            'Meta': {'object_name': 'DaysLog'},
            'day': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'happenings': ('django.db.models.fields.TextField', [], {'default': "'<h1>Things that happened today</h1>\\n<ol>\\n  <li>Clock ticked over midnight.</li>\\n</ol>'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['dayslog']
# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scribble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=255, blank=True)),
                ('slug', models.SlugField(default='', max_length=64, blank=True)),
                ('url', models.CharField(default='', max_length=255, blank=True)),
                ('content', models.TextField(default='', blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='scribble',
            unique_together=set([('slug', 'url')]),
        ),
    ]

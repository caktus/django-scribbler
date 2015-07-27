# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DaysLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField(unique=True)),
                ('happenings', models.TextField(default=b'<h1>Things that happened today</h1>\n<ol>\n  <li>Clock ticked over midnight.</li>\n</ol>')),
            ],
        ),
    ]

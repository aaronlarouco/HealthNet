# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEvent',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('source', models.CharField(max_length=64)),
                ('action', models.CharField(max_length=64)),
                ('eventCode', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=10)),
                ('message', models.TextField()),
            ],
        ),
    ]

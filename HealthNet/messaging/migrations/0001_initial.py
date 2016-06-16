# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('subject', models.CharField(null=True, blank=True, max_length=200)),
                ('body', models.TextField()),
                ('send_date_time', models.DateTimeField()),
                ('was_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(to='profiles.HealthNetUser', related_name='receiver')),
                ('reply', models.OneToOneField(null=True, to='messaging.Message')),
                ('sender', models.ForeignKey(to='profiles.HealthNetUser', related_name='sender')),
            ],
        ),
    ]

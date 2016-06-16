# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=32)),
                ('startDate', models.DateField()),
                ('startTime', models.CharField(max_length=10)),
                ('endDate', models.DateField()),
                ('endTime', models.CharField(max_length=10)),
                ('room', models.CharField(max_length=32)),
                ('reason', models.TextField()),
                ('status', models.CharField(default='P', choices=[('P', 'Pending Approval'), ('A', 'Approved'), ('D', 'Denied'), ('C', 'Cancelled')], max_length=1)),
                ('notes', models.TextField(null=True)),
                ('case', models.ForeignKey(to='profiles.MedicalCase', null=True)),
                ('doctor', models.ForeignKey(to='profiles.Staff')),
                ('hospital', models.ForeignKey(to='profiles.Hospital')),
                ('patient', models.ForeignKey(to='profiles.Patient')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import profiles.helpers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('firstName', models.CharField(max_length=32)),
                ('middleInitial', models.CharField(null=True, blank=True, max_length=1)),
                ('lastName', models.CharField(max_length=64)),
                ('phoneNumber', models.CharField(max_length=14)),
                ('street', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=32)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
                ('relation', models.CharField(choices=[('ga', 'Guardian'), ('sp', 'Spouse'), ('fa', 'Father'), ('mo', 'Mother'), ('si', 'Sibling'), ('ch', 'Child'), ('ot', 'Other'), ('se', 'Self')], max_length=2)),
                ('type', models.CharField(choices=[('e', 'Emergency'), ('d', 'Doctor'), ('n', 'Nurse'), ('p', 'Patient')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('drugId', models.CharField(max_length=64)),
                ('usage', models.TextField()),
                ('sideEffects', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HealthNetUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('accountType', models.CharField(default='P', choices=[('P', 'Patient'), ('D', 'Doctor'), ('A', 'Admin'), ('N', 'Nurse')], max_length=1)),
                ('isNew', models.BooleanField(default=True)),
                ('shownTutorial', models.BooleanField(default=False)),
                ('photo', models.ImageField(default='/static/images/profile.png', upload_to=profiles.helpers.randomPhotoName)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('street', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=32)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('numVisits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Illness',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('illnessId', models.CharField(max_length=64)),
                ('symptoms', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MedicalCase',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=64)),
                ('caseId', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('notes', models.TextField(null=True, blank=True)),
                ('ongoing', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('file', models.FileField(upload_to=profiles.helpers.randomFileName)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('startDate', models.DateField()),
                ('refills', models.IntegerField()),
                ('dose', models.TextField()),
                ('pharmacy', models.CharField(max_length=64)),
                ('drug', models.ForeignKey(to='profiles.Drug')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('healthnetuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='profiles.HealthNetUser', primary_key=True, serialize=False)),
                ('birthDate', models.DateField()),
                ('heightFeet', models.IntegerField()),
                ('heightInches', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('insuranceCompany', models.CharField(max_length=200)),
                ('insuranceId', models.CharField(max_length=200)),
                ('numVisits', models.IntegerField(default=1)),
                ('hospital', models.ForeignKey(null=True, to='profiles.Hospital', related_name='hospital')),
                ('hospitalPref', models.ForeignKey(null=True, to='profiles.Hospital', related_name='hospitalPref')),
            ],
            bases=('profiles.healthnetuser',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('healthnetuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='profiles.HealthNetUser', primary_key=True, serialize=False)),
                ('bio', models.TextField(null=True)),
                ('hospital', models.ForeignKey(to='profiles.Hospital')),
            ],
            bases=('profiles.healthnetuser',),
        ),
        migrations.AddField(
            model_name='medicalcase',
            name='files',
            field=models.ManyToManyField(to='profiles.PatientFile', blank=True),
        ),
        migrations.AddField(
            model_name='medicalcase',
            name='illness',
            field=models.ForeignKey(to='profiles.Illness'),
        ),
        migrations.AddField(
            model_name='medicalcase',
            name='prescriptions',
            field=models.ManyToManyField(to='profiles.Prescription', blank=True),
        ),
        migrations.AddField(
            model_name='healthnetuser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drug',
            name='illnesses',
            field=models.ManyToManyField(to='profiles.Illness'),
        ),
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(to='profiles.HealthNetUser'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(to='profiles.Staff'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(to='profiles.Patient'),
        ),
        migrations.AddField(
            model_name='patientfile',
            name='patient',
            field=models.ForeignKey(to='profiles.Patient'),
        ),
        migrations.AddField(
            model_name='medicalcase',
            name='patient',
            field=models.ForeignKey(to='profiles.Patient'),
        ),
    ]

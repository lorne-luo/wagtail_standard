# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-01 04:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0020_auto_20180301_0339'),
        ('wagtailcore', '0041_auto_20180301_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='contactor name', max_length=255, verbose_name='name')),
                ('address1', models.CharField(blank=True, help_text='address1', max_length=255, verbose_name='address1')),
                ('address2', models.CharField(blank=True, help_text='address2', max_length=255, verbose_name='address2')),
                ('city', models.CharField(blank=True, choices=[('Sydney', 'Sydney'), ('Melbourne', 'Melbourne'), ('Adelaide', 'Adelaide'), ('Hobart', 'Hobart'), ('Hobart', 'Hobart'), ('Darwin', 'Darwin'), ('Canberra', 'Canberra')], help_text='city', max_length=255, verbose_name='city')),
                ('state', models.CharField(blank=True, choices=[('NSW', 'NSW'), ('VIC', 'VIC'), ('QLD', 'QLD'), ('TAS', 'TAS'), ('WA', 'WA'), ('ACT', 'ACT'), ('NT', 'NT')], help_text='state', max_length=255, verbose_name='state')),
                ('postcode', models.CharField(blank=True, help_text='postcode', max_length=32, verbose_name='postcode')),
                ('phone', models.CharField(blank=True, help_text='phone', max_length=32, verbose_name='phone')),
                ('email', models.EmailField(blank=True, help_text='email', max_length=255, verbose_name='email')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'contact us',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Partner name', max_length=255, verbose_name='name')),
                ('link', models.URLField(blank=True, help_text='Partner link', verbose_name='link')),
                ('class_name', models.CharField(blank=True, help_text='styling class name', max_length=64, verbose_name='styling class name')),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
        ),
    ]
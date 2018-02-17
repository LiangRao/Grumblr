# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 11:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0003_auto_20161009_1005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='followees',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='follower',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(related_name='followees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Follower',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reporter', '0003_rendering_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rendering',
            name='html',
        ),
        migrations.RemoveField(
            model_name='rendering',
            name='md',
        ),
        migrations.RemoveField(
            model_name='rendering',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='template',
            name='name',
        ),
        migrations.AddField(
            model_name='template',
            name='slug',
            field=models.SlugField(default=b''),
        ),
        migrations.AddField(
            model_name='template',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='rendering',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

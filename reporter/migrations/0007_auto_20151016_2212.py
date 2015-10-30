# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0006_auto_20150910_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='user',
        ),
        migrations.AddField(
            model_name='template',
            name='name',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='template',
            name='slug',
            field=models.SlugField(default=b'', unique=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendering',
            name='api_token',
            field=models.TextField(blank=True),
        ),
    ]

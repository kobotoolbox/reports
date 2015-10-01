# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equitytool', '0004_auto_20151001_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='csv_form',
            field=models.TextField(default=b''),
        ),
    ]

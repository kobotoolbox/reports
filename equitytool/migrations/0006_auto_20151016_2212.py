# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equitytool', '0005_form_csv_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='csv_form',
            field=models.TextField(default=b'', blank=True),
        ),
    ]

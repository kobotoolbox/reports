# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equitytool', '0003_remove_form_csv_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]

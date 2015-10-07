# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equitytool', '0002_form_xls_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='csv_form',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equitytool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='xls_form',
            field=models.FileField(default=None, upload_to=b''),
        ),
    ]

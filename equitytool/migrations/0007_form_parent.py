# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equitytool', '0006_auto_20151016_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='parent',
            field=models.ForeignKey(blank=True, to='equitytool.Form', null=True),
        ),
    ]

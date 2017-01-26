# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0010_auto_20160219_2058'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rendering',
            unique_together=set([('user', 'name')]),
        ),
    ]

# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0008_auto_20151016_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendering',
            name='_enter_data_link',
            field=models.URLField(blank=True),
        ),
    ]

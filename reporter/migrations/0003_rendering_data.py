# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0002_rendering_api_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendering',
            name='data',
            field=models.TextField(default=b''),
        ),
    ]

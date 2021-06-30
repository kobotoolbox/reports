# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0004_auto_20150813_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rendering',
            name='user',
            field=models.ForeignKey(
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AlterField(
            model_name='template',
            name='user',
            field=models.ForeignKey(
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
    ]

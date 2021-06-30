# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0005_auto_20150813_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendering',
            name='created',
            field=models.DateTimeField(
                default=datetime.datetime(
                    2015, 9, 10, 17, 20, 58, 817285, tzinfo=utc
                ),
                auto_now_add=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rendering',
            name='modified',
            field=models.DateTimeField(
                default=datetime.datetime(
                    2015, 9, 10, 17, 21, 11, 345357, tzinfo=utc
                ),
                auto_now=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rendering',
            name='name',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='rendering',
            name='user',
            field=models.ForeignKey(
                related_name='renderings',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.CASCADE,
            ),
        ),
    ]

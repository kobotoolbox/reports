# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0009_rendering__enter_data_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendering',
            name='form_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='rendering',
            name='form_pk',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

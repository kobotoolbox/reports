# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reporter', '0007_auto_20151016_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExternalApiToken',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID',
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ('key', models.CharField(max_length=120)),
                (
                    'user',
                    models.OneToOneField(
                        related_name='external_api_token',
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name='rendering',
            name='api_token',
        ),
    ]

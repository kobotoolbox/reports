# Generated by Django 3.2 on 2021-05-18 14:29

from django.db import migrations, models
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('equitytool', '0008_upgrades_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminStatsReportTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'new'), ('pending', 'pending'), ('complete', 'complete'), ('failed', 'failed')], default='new', max_length=16)),
                ('result', private_storage.fields.PrivateFileField(default=None, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='')),
            ],
        ),
    ]
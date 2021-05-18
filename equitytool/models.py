from django.db import models
from private_storage.fields import PrivateFileField
from .tasks import generate_admin_stats
from .xls2csv import xls2csv


class Form(models.Model):
    """
    An administrator-defined form that regular users can select when they
    create new projects. The form is then sent to the regular user's linked
    KoBoToolbox account, creating a new project that, in turn, is referenced by
    a `reporter.Rendering`
    """
    # `name` means country name in the current implementation
    name = models.CharField(max_length=255, unique=True)
    xls_form = PrivateFileField(default=None)
    csv_form = models.TextField(
        default='', blank=True, help_text='Always overwritten by `xls_form`'
    )
    parent = models.ForeignKey(
        'equitytool.Form', null=True, blank=True, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        settings = {
            'form_title': '{{ form_title }}',
            'form_id': '{{ form_id }}',
        }
        self.csv_form = xls2csv(self.xls_form, **settings)
        super(Form, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class AdminStatsReportTask(models.Model):
    """
    Run print_stats management command asynchronously and allow jobs to be
    started through the admin interface
    """
    NEW = 'new'
    PENDING = 'pending'
    COMPLETE = 'complete'
    FAILED = 'failed'
    status = models.CharField(
        max_length=16,
        default=NEW,
        choices=(
            (choice, choice) for choice in (NEW, PENDING, COMPLETE, FAILED)
        ),
    )
    result = PrivateFileField(default=None)

    def __str__(self):
        blurb = f'{self.status} report'
        if self.result:
            return f'{blurb} ({self.result})'
        if self.pk:
            return f'{blurb} ({self.pk})'

    def save(self, *args, **kwargs):
        created = False
        if self.pk is None:
            created = True
        super().save(*args, **kwargs)
        if created:
            generate_admin_stats(self.pk)

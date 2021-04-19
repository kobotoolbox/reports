from django.db import models
from private_storage.fields import PrivateFileField
from .xls2csv import xls2csv


class Form(models.Model):
    ''' An administrator-defined form that regular users can select when they
    create new projects. The form is then POSTed to KoBoCAT, creating a new
    XForm under the regular user's account there. That XForm, in turn, will be
    referenced by a `reporter.Rendering` '''
    # `name` means country name in the current implementation
    name = models.CharField(max_length=255, unique=True)
    xls_form = PrivateFileField(default=None)
    csv_form = models.TextField(
        default='', blank=True, help_text='Always overwritten by `xls_form`')
    parent = models.ForeignKey('equitytool.Form', null=True, blank=True)

    def save(self, *args, **kwargs):
        settings = {
            'form_title': '{{ form_title }}',
            'form_id': '{{ form_id }}',
        }
        self.csv_form = xls2csv(self.xls_form, **settings)
        super(Form, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

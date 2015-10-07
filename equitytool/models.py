from django.db import models
from xls2csv import xls2csv


class Form(models.Model):
    name = models.CharField(max_length=255, unique=True)
    xls_form = models.FileField(default=None)
    csv_form = models.TextField(default='', blank=True)

    def save(self, *args, **kwargs):
        settings = {
            'form_title': '{{ form_title }}',
            'form_id': '{{ form_id }}',
        }
        self.csv_form = xls2csv(self.xls_form, **settings)
        super(Form, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

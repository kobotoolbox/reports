from django.db import models
from xls2csv import xls2csv


class Form(models.Model):
    name = models.TextField(unique=True)
    csv_form = models.TextField(blank=True)
    xls_form = models.FileField(default=None)

    def save(self, *args, **kwargs):
        self.csv_form = xls2csv(self.xls_form)
        super(Form, self).save(*args, **kwargs)

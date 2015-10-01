from django.db import models
from xls2csv import xls2csv


class Form(models.Model):
    name = models.CharField(max_length=255, unique=True)
    xls_form = models.FileField(default=None)

    def __unicode__(self):
        return self.name

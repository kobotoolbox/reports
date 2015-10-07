from django.contrib import admin
from .models import Form


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass

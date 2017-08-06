from django.contrib import admin
from .models import Form


class ChildFormInline(admin.StackedInline):
    model = Form
    show_change_link = True
    can_delete = False
    extra = 0

    def get_fields(*args, **kwargs):
        # Don't show any fields at all. Without overriding this method, a falsy
        # `fields` value causes all fields to be shown
        return []

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [ChildFormInline]

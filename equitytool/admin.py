from django.contrib import admin
from .models import Form


class ChildFormInline(admin.StackedInline):
    model = Form
    show_change_link = True
    can_delete = False
    extra = 0
    verbose_name = 'child form'
    verbose_name_plural = verbose_name + 's'

    def get_fields(*args, **kwargs):
        # Don't show any fields at all. Without overriding this method, a falsy
        # `fields` value causes all fields to be shown
        return []

    def has_add_permission(*args, **kwargs):
        # For simplicity, don't allow adding child forms via the inline. They
        # would not automatically have their `parent` field set correctly
        return False

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [ChildFormInline]
    readonly_fields = ('csv_form',)

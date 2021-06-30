from django.contrib import admin
from .models import Form, AdminStatsReportTask


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

    def get_form(self, *args, **kwargs):
        form = super(FormAdmin, self).get_form(*args, **kwargs)
        # Encourage the user not to edit the `csv_form` field. This `form` is a
        # `django.forms.models.ModelFormMetaclass`, not an instance, so it does
        # not have a `fields` attribute
        form.base_fields['csv_form'].widget.attrs['disabled'] = True
        return form


@admin.register(AdminStatsReportTask)
class AdminStatsReportTaskAdmin(admin.ModelAdmin):
    instructions = (
        'If "Result" is empty, click "SAVE" to start generating a new report. '
        'After that, refresh the page periodically until the report completes.'
    )
    readonly_fields = ['result']
    fieldsets = (
        (instructions, {'fields': ('result',)}),
    )

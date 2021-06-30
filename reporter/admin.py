from django.contrib import admin
from .models import Template, Rendering


class TemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Template, TemplateAdmin)


class RenderingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Rendering, RenderingAdmin)

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def forgot_password_url():
    return settings.KPI_URL + 'accounts/password/reset/'

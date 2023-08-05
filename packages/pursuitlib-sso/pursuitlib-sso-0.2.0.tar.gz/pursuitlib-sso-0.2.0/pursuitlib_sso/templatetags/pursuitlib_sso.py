from django import template
from django.conf import settings

from django.urls import reverse

from pursuitlib_sso import urls

# Read the Django configuration

BASE_URL = getattr(settings, "BASE_URL")


register = template.Library()


@register.simple_tag
def sso_url(name: str) -> str:
    return BASE_URL + reverse(name, current_app=urls.SSO_NAME)

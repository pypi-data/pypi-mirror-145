from django.apps import AppConfig
from django.urls import path

from pursuitlib_sso import views


class PursuitlibSsoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pursuitlib_sso'

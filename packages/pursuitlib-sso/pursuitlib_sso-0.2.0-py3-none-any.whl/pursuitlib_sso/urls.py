from django.urls import path

from . import views

SSO_NAMESPACE = "sso"
SSO_NAME = "pursuitlib_sso"


def get_urls():
    return [
        path("saml2/metadata.xml", views.saml2_metadata, name="saml2_metadata"),
        path("saml2/acs", views.saml2_acs, name="saml2_acs"),
        path("saml2/<str:idp>", views.saml2, name="saml2"),
    ]


def include_urls():
    return get_urls(), SSO_NAMESPACE, SSO_NAME

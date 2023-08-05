import base64
import urllib.parse as urlparse
import xml.etree.ElementTree as et
from typing import Optional, Dict
from urllib.parse import unquote

from django.conf import settings
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import redirect, resolve_url, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from saml2 import entity, BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config

from pursuitlib_sso import urls

# Read the Django configuration

BASE_URL = getattr(settings, "BASE_URL")
ALLOWED_HOSTS = getattr(settings, "ALLOWED_HOSTS")
DEBUG = getattr(settings, "DEBUG")
SSO_CONFIG = getattr(settings, "SSO_CONFIG")
SSO_DEBUG = getattr(settings, "SSO_DEBUG", False)
SAML2_CONFIG = SSO_CONFIG["saml2"]
DEFAULT_REDIRECT = SSO_CONFIG["default_redirect"]
get_or_create_user = SSO_CONFIG["get_or_create_user"]


# Views

def saml2_metadata(request: HttpRequest) -> HttpRequest:
    return render(request, "pursuitlib/sso/saml2-metadata.xml", context={"config": SAML2_CONFIG}, content_type="application/xml")


@csrf_exempt
def saml2_acs(request: HttpRequest) -> HttpResponse:
    next_url = request.session.get('login_next_url', resolve_url(DEFAULT_REDIRECT))

    if not request.user.is_anonymous:
        return HttpResponseRedirect(next_url)

    if DEBUG and SSO_DEBUG:
        idp_id = request.GET.get("idp", None)
        if not idp_id:
            raise PermissionDenied()

        idp = get_idp_by_id(idp_id)
        user_identity = idp["debug_identity"]
    else:
        resp = request.POST.get("SAMLResponse", None)
        if not resp:
            raise PermissionDenied()

        idp = get_idp_by_entity(get_idp_entity(resp))
        saml_client = get_saml_client(idp)
        if saml_client is None:
            raise PermissionDenied()

        authn_response = saml_client.parse_authn_request_response(resp, entity.BINDING_HTTP_POST)
        if authn_response is None:
            raise PermissionDenied()

        raw_identity = authn_response.get_identity()
        if raw_identity is None:
            raise PermissionDenied()

        # The raw identitiy contains lists of attribute values. For each attribute, we only need one
        user_identity = {}
        for key, value in raw_identity.items():
            user_identity[key] = value[0]

    user_data = get_user_data(user_identity, idp["mapping"] if "mapping" in idp else {})
    user = get_or_create_user(idp["id"], user_data)
    request.session.flush()

    if user.is_active:
        login(request, user)
    else: raise PermissionDenied()

    return HttpResponseRedirect(next_url)


def saml2(request: HttpRequest, idp: str) -> HttpResponse:
    next_url = request.GET.get('next', resolve_url(DEFAULT_REDIRECT))
    if 'next=' in unquote(next_url):
        next_url = urlparse.parse_qs(urlparse.urlparse(unquote(next_url)).query)['next'][0]

    if not request.user.is_anonymous:
        return HttpResponseRedirect(next_url)

    if not url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
        raise PermissionDenied()

    request.session['login_next_url'] = next_url

    if DEBUG and SSO_DEBUG:
        return HttpResponseRedirect(resolve_url("sso:saml2_acs") + f"?idp={idp}")
    else:
        saml_client = get_saml_client(get_idp_by_id(idp))
        if saml_client is None:
            raise Http404()

        _, info = saml_client.prepare_for_authenticate()

        redirect_url = None

        for key, value in info['headers']:
            if key == 'Location':
                redirect_url = value
                break

        return HttpResponseRedirect(redirect_url)


# Utility functions

def get_idp_by_id(idp_id: str):
    for idp in SAML2_CONFIG["idp"]:
        if idp["id"] == idp_id:
            return idp
    raise Http404()


def get_idp_by_entity(idp_entity: str):
    for idp in SAML2_CONFIG["idp"]:
        if idp["entity"] == idp_entity:
            return idp
    raise Http404()


def get_user_data(user_identity: Dict[str, str], mapping: Dict[str, str]) -> Dict[str, Optional[str]]:
    data = {}
    for key, value in user_identity.items():
        mapped_key = mapping[key] if key in mapping else key
        data[mapped_key] = value
    return data


def get_saml_client(idp):
    if idp is None:
        return None

    saml_settings = {
        'metadata': {
            'remote': [
                {
                    "url": idp["metadata"]
                },
            ]
        },
        'service': get_saml2_service_settings(),
        'entityid': SAML2_CONFIG["entityid"]
    }

    sp_config = Saml2Config()
    sp_config.load(saml_settings)
    sp_config.allow_unknown_attributes = True
    saml_client = Saml2Client(config=sp_config)
    return saml_client


def get_idp_entity(response):
    xml = base64.b64decode(response)
    tree = et.fromstring(xml)
    issuer = tree.find('{urn:oasis:names:tc:SAML:2.0:assertion}Issuer')
    return issuer.text if issuer is not None else None


def get_acs_url() -> str:
    return BASE_URL + reverse("sso:saml2_acs", current_app=urls.SSO_NAME)


def get_saml2_service_settings():
    return {
        'sp': {
            'endpoints': {
                'assertion_consumer_service': [
                    (get_acs_url(), BINDING_HTTP_REDIRECT),
                    (get_acs_url(), BINDING_HTTP_POST)
                ],
            },
            'allow_unsolicited': True,
            'authn_requests_signed': False,
            'logout_requests_signed': True,
            'want_assertions_signed': True,
            'want_response_signed': False,
        },
    }

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from django.conf import settings
from django.utils.module_loading import import_string

from ideler_mfa.settings import SESSION_KEYS


def get_issuer_name():
    try:
        return settings.IDELER_MFA["ISSUER_NAME"]
    except (AttributeError, KeyError):
        return None


def get_username(user):
    return getattr(user, user.USERNAME_FIELD)


def get_redirect_url():
    try:
        url = settings.IDELER_MFA["CONFIGURATION_REDIRECT_URL"]
    except (AttributeError, KeyError):
        try:
            url = settings.LOGIN_REDIRECT_URL
        except AttributeError:
            url = "/"
    return url


def get_allowed_names():
    try:
        return settings.IDELER_MFA["ALLOWED_NAMES"]
    except (AttributeError, KeyError):
        return ['logout']


def import_otp_method(method):
    if isinstance(method, str):
        return import_string(method)
    return None


def clear_session_keys(request):
    for _, key in SESSION_KEYS.items():
        if key in request.session:
            del request.session[key]

#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django.urls import resolve
from django.shortcuts import resolve_url

from ideler_mfa.models import is_mfa_enabled
from ideler_mfa.settings import VERIFIED_SESSION_KEY
from ideler_mfa.utils import get_allowed_names


class MFAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if is_mfa_enabled(request.user):
                if not request.session.get(VERIFIED_SESSION_KEY):
                    if not self._is_allowed_url(request):
                        path = request.get_full_path()
                        resolved_login_url = resolve_url(
                            reverse("ideler_mfa:verify")
                        )
                        return redirect_to_login(
                            path, resolved_login_url, REDIRECT_FIELD_NAME
                        )
        return self.get_response(request)

    def _is_allowed_url(self, request):
        resolved = resolve(request.path_info)

        if 'ideler_mfa' in resolved.namespaces:
            return True

        if resolved.url_name in get_allowed_names():
            return True

        return False

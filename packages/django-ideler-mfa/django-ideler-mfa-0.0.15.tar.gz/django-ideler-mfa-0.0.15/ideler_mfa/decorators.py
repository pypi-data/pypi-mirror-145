#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from functools import wraps

from django.shortcuts import redirect
from django.shortcuts import resolve_url

from ideler_mfa.models import is_mfa_enabled
from ideler_mfa.utils import clear_session_keys as _clear_session_keys
from ideler_mfa.utils import get_redirect_url


def _user_passes_test(test_func, redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            resolved_url = resolve_url(redirect_url or get_redirect_url())
            return redirect(resolved_url)

        return _wrapped_view

    return decorator


def requires_mfa_enabled(view_func=None, redirect_url="ideler_mfa:disable"):
    actual_decorator = _user_passes_test(
        lambda u: is_mfa_enabled(u), redirect_url=redirect_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def requires_mfa_disabled(view_func=None, redirect_url="ideler_mfa:select"):
    actual_decorator = _user_passes_test(
        lambda u: not is_mfa_enabled(u), redirect_url=redirect_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def clear_session_keys(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        _clear_session_keys(request)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def session_key_required(key, redirect_url="ideler_mfa:select"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if key not in request.session:
                resolved_url = resolve_url(redirect_url or get_redirect_url())
                return redirect(resolved_url)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

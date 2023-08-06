#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import RedirectView

from ideler_mfa.decorators import clear_session_keys
from ideler_mfa.decorators import requires_mfa_disabled
from ideler_mfa.decorators import requires_mfa_enabled
from ideler_mfa.decorators import session_key_required
from ideler_mfa.forms import OneTimePasswordConfigurationForm
from ideler_mfa.forms import OneTimePasswordForm
from ideler_mfa.forms import OneTimePasswortSelectMethodForm
from ideler_mfa.methods import GenericOTP
from ideler_mfa.models import OneTimePassword
from ideler_mfa.settings import SESSION_KEYS
from ideler_mfa.settings import VERIFIED_SESSION_KEY
from ideler_mfa.utils import get_redirect_url
from ideler_mfa.utils import import_otp_method


def _session_key_required(key):
    return method_decorator(session_key_required(key), name="dispatch")


@method_decorator(clear_session_keys, name="dispatch")
@method_decorator(login_required, name="dispatch")
@method_decorator(requires_mfa_disabled, name="dispatch")
class SelectMFAView(FormView):
    template_name = "ideler_mfa/select.html"
    form_class = OneTimePasswortSelectMethodForm

    def get_success_url(self):
        method = self.request.session[SESSION_KEYS["method"]]
        otp_class = import_otp_method(method)
        if otp_class.configuration_required:
            return reverse("ideler_mfa:configure")
        else:
            return reverse("ideler_mfa:enable")

    def form_valid(self, form):
        method = form.cleaned_data.get("method")
        self.request.session[SESSION_KEYS["method"]] = method
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(requires_mfa_disabled, name="dispatch")
@_session_key_required(SESSION_KEYS["method"])
class ConfigureMFAView(FormView):
    template_name = "ideler_mfa/configure.html"
    form_class = OneTimePasswordConfigurationForm

    def get_secret(self):
        if not getattr(self, "_secret", None):
            self._secret = self.request.session.get(
                SESSION_KEYS["secret_key"], GenericOTP.generate_secret_utf8()
            )
            self.request.session[SESSION_KEYS["secret_key"]] = self._secret
        return self._secret

    def get_method(self):
        if not getattr(self, "_method", None):
            self._method = self.request.session.get(SESSION_KEYS["method"])
        return self._method

    def get_otp_obj(self):
        if not getattr(self, "_otp_obj", None):
            secret = self.get_secret()
            method = self.get_method()
            self._otp_obj = import_otp_method(method)(secret,
                                                      self.request.user)
        return self._otp_obj

    def get_initial(self):
        initial = super().get_initial()
        secret = self.get_secret()
        method = self.get_method()
        initial.update({"secret_key": secret, "method": method})
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        otp_obj = self.get_otp_obj()
        qr_info = otp_obj.provisioning_uri()
        context.update({"qr_info": qr_info})
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("ideler_mfa:enable")

    def form_valid(self, form):
        self.request.session[SESSION_KEYS["method_configured"]] = True
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(requires_mfa_disabled, name="dispatch")
@_session_key_required(SESSION_KEYS["method"])
@_session_key_required(SESSION_KEYS["secret_key"])
class EnableMFAView(RedirectView):
    def enable_mfa(self):
        session = self.request.session
        method = session.get(SESSION_KEYS["method"])
        secret = session.get(SESSION_KEYS["secret_key"])
        OneTimePassword.objects.create(
            user=self.request.user, method=method, secret_key=secret
        )
        session[VERIFIED_SESSION_KEY] = True
        messages.success(
            self.request,
            _(
                "You have successfully enabled multi-factor"
                " authentication on your account."
            ),
        )
        return True

    def get_redirect_url(self, *args, **kwargs):
        if getattr(self, "mfa_enabled", False):
            return resolve_url(get_redirect_url())
        else:
            return reverse("ideler_mfa:select")

    def get(self, request, *args, **kwargs):
        method = self.request.session.get(SESSION_KEYS["method"])
        self.otp_class = import_otp_method(method)
        if self.otp_class.configuration_required:
            method_configured_key = SESSION_KEYS["method_configured"]
            if not self.request.session.get(method_configured_key, False):
                return super().get(request, *args, **kwargs)
        self.mfa_enabled = self.enable_mfa()
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
@method_decorator(requires_mfa_enabled, name="dispatch")
class DisableMFAView(DeleteView):
    template_name = "ideler_mfa/disable.html"

    def get_success_url(self):
        return resolve_url(get_redirect_url())

    def get_object(self):
        return self.request.user.otp

    def delete(self, request, *args, **kwargs):
        session = self.request.session
        if VERIFIED_SESSION_KEY in session:
            del session[VERIFIED_SESSION_KEY]
        for session_key in SESSION_KEYS.values():
            if session_key in session:
                del session[session_key]
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
@method_decorator(requires_mfa_enabled, name="dispatch")
class VerifyMFAView(FormView):
    template_name = "ideler_mfa/verify.html"
    form_class = OneTimePasswordForm

    def get(self, request, *args, **kwargs):
        secret = self.request.user.otp.secret_key
        method = self.request.user.otp.method
        self.otp_obj = import_otp_method(method)(secret, self.request.user)
        self.otp_obj.notify()
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_success_url(self):
        next_url = self.request.GET.get(
            REDIRECT_FIELD_NAME, get_redirect_url()
        )
        return resolve_url(next_url)

    def form_valid(self, form):
        session = self.request.session
        session[VERIFIED_SESSION_KEY] = True
        return super().form_valid(form)

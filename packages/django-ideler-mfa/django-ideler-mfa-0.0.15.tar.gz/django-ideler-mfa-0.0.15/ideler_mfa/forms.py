#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ideler_mfa.utils import import_otp_method


def get_available_methods():
    try:
        return settings.IDELER_MFA["OTP_TYPES"]
    except (
        AttributeError,
        KeyError,
    ):
        return ("ideler_mfa.methods.TOTP",)


def get_mehod_choices():
    methods = get_available_methods()
    for method in methods:
        otp_class = import_otp_method(method)
        yield (method, otp_class.verbose_name)


class OneTimePasswortSelectMethodForm(forms.Form):
    method = forms.ChoiceField(label=_("Method"), choices=get_mehod_choices())


class BaseOneTimePasswordForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        label=_("Verification code"),
        widget=forms.TextInput(
            attrs={"autofocus": True, "autocomplete": False}
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def get_secret(self, cleaned_data):
        raise NotImplementedError

    def get_method(self, cleaned_data):
        raise NotImplementedError

    def clean(self):
        cleaned_data = super().clean()
        secret = self.get_secret(cleaned_data)
        method = self.get_method(cleaned_data)
        verification_code = self.cleaned_data.get("verification_code")
        otp_obj = import_otp_method(method)(secret, self.user)
        is_verified = otp_obj.verify(verification_code)
        if not is_verified:
            self.add_error(
                "verification_code",
                _("The verification code you entered was incorrect."),
            )
        return cleaned_data


class OneTimePasswordForm(BaseOneTimePasswordForm):
    def get_secret(self, cleaned_data):
        return self.user.otp.secret_key

    def get_method(self, cleaned_data):
        return self.user.otp.method


class OneTimePasswordConfigurationForm(BaseOneTimePasswordForm):
    method = forms.ChoiceField(
        choices=get_mehod_choices(), widget=forms.HiddenInput()
    )
    secret_key = forms.CharField(max_length=100, widget=forms.HiddenInput())

    def get_secret(self, cleaned_data):
        return self.cleaned_data.get("secret_key")

    def get_method(self, cleaned_data):
        return self.cleaned_data.get("method")


class OneTimePasswordDisableForm(forms.Form):
    pass

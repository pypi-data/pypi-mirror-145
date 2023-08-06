#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import pyotp

from django.utils.translation import gettext_lazy as _

from ideler_mfa.methods.otp import GenericOTP
from ideler_mfa.utils import get_username
from ideler_mfa.utils import get_issuer_name


class TOTP(GenericOTP):
    """
    :param interval: Interval for TOTP. Default is 30.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        interval = kwargs.pop("interval", 30)
        self.totp_obj = pyotp.TOTP(self.secret, interval=interval)

    verbose_name = _("Time-based one-time password")
    configuration_required = True

    def provisioning_uri(self):
        """
        Returns the provisioning URI for the OTP.  This can then be
        encoded in a QR Code and used to provision an OTP app like
        Google Authenticator.

        See also:
            https://github.com/google/google-authenticator/wiki/Key-Uri-Format

        """
        username = get_username(self.user)
        issuer_name = get_issuer_name()
        return self.totp_obj.provisioning_uri(
            username, issuer_name=issuer_name
        )

    def notify(self):
        pass

    def verify(self, verification_code):
        return self.totp_obj.verify(verification_code)

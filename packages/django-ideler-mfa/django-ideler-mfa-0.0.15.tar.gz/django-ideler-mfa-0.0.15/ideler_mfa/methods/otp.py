#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import base64
import codecs
import random


class GenericOTP:
    """
    :param secret: The secret for generating and validating tokens.
    """

    def __init__(self, secret, user, *args, **kwargs):
        self.secret = secret
        self.user = user

    verbose_name = "Generic one-time password"
    configuration_required = True

    def provisioning_uri(self):
        raise NotImplementedError

    def notify(self):
        raise NotImplementedError

    def verify(self, verification_code):
        raise NotImplementedError

    @classmethod
    def generate_secret_utf8(cls):
        return base64.b32encode(
            codecs.decode(
                codecs.encode("{0:020x}".format(random.getrandbits(80))),
                "hex_codec",
            )
        ).decode("utf-8")

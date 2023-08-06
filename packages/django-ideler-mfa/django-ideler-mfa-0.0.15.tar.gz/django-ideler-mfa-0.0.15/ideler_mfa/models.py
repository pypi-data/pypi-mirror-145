#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class OneTimePassword(models.Model):
    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name="otp"
    )
    method = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=100, blank=True)

    config = models.TextField(blank=True)

    def __str__(self):
        return str(self.user)


def is_mfa_enabled(user):
    otp_enabled = hasattr(user, "otp")
    return otp_enabled


class RecoveryCode(models.Model):
    user = models.ForeignKey("OneTimePassword", on_delete=models.CASCADE)
    secret_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user)

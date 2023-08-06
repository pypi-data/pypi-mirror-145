#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from django.contrib import admin

from ideler_mfa.models import OneTimePassword
from ideler_mfa.models import RecoveryCode


admin.site.register(OneTimePassword)
admin.site.register(RecoveryCode)

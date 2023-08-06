#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from django.urls import path

from ideler_mfa.views import SelectMFAView
from ideler_mfa.views import ConfigureMFAView
from ideler_mfa.views import EnableMFAView
from ideler_mfa.views import DisableMFAView
from ideler_mfa.views import VerifyMFAView

app_name = "ideler_mfa"
namespace = "ideler_mfa"
urlpatterns = [
    path("select/", SelectMFAView.as_view(), name="select"),
    path("configure/", ConfigureMFAView.as_view(), name="configure"),
    path("enable/", EnableMFAView.as_view(), name="enable"),
    path("disable/", DisableMFAView.as_view(), name="disable"),
    path("verify/", VerifyMFAView.as_view(), name="verify"),
]

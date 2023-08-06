#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import segno
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def qr_code(
    content,
    size=5,
    border=None,
    dark="black",
    light=None,
    micro=False,
    **kwargs
):
    kwargs.update({"micro": micro})
    qr = segno.make(content, **kwargs)
    result = qr.svg_inline(scale=size, dark=dark, light=light)
    return mark_safe(result)


@register.filter
def is_mfa_enabled(user):
    return hasattr(user, "otp")

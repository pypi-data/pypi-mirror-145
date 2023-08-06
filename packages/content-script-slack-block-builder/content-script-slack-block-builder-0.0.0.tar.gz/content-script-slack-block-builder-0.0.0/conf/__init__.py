#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : __init__.py
# @Date : 2021-12-17-21-11
# @Project: content-service-chat-assistant

from os import environ

PROFILE = environ.get('PROFILE', 'dev')

if PROFILE == "prod":
    from conf.prod import *
else:
    from conf.dev import *


def get(name, default=None):
    import conf as this_module
    return getattr(this_module, name, default)

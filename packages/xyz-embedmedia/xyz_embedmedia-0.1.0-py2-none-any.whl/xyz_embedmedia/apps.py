# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class Config(AppConfig):
    name = 'xyz_embedmedia'
    label = 'embedmedia'
    verbose_name = '内嵌媒体'

    def ready(self):
        super(Config, self).ready()
        # from .helper import cache_vendors_expire_time
        # cache_vendors_expire_time()

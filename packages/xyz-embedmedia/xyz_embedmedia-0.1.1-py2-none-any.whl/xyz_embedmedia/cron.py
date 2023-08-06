# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from .models import Testing
from datetime import datetime
import logging

log = logging.getLogger('django')


def run_testing():
    now = datetime.now()
    for t in Testing.objects.filter(next_time__lt=now, is_active=True):
        try:
            log.info('embedmedia run_testing: %s %s: %s', t.vendor, t.name, t.url)
            t.run()
        except:
            import traceback
            log.error('embedmedia vendor %s run_testing %s error: %s', t.vendor, t, traceback.format_exc())

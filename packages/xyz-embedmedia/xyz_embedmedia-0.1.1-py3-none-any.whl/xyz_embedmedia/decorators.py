# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from .vendor import register as reg

def register(**kwargs):
    def _vendor_wrapper(vendor_class):
        reg(vendor_class)
        return vendor_class

    return _vendor_wrapper

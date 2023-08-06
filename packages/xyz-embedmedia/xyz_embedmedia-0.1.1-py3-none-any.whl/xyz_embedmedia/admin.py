# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from .models import *


# Register your models here.

@admin.decorators.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_expire_minutes', 'update_time', 'create_time')
    search_fields = ('name', )
    readonly_fields = ('average_expire_minutes',)

@admin.decorators.register(Testing)
class TestingAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'explain_time', 'last_minutes', 'expire_time', 'expire_minutes', 'next_time', 'update_time', 'create_time')
    search_fields = ('name', 'url')
    readonly_fields = ('average_expire_minutes',)
    list_filter = ('is_active', 'type')
    raw_id_fields = ('vendor', )


@admin.decorators.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('url', 'name', 'vendor', 'media_type', 'expire_time', 'create_time')
    search_fields = ('name', 'url')
    list_filter = ('media_type', )
    raw_id_fields = ('vendor',)

@admin.decorators.register(Browse)
class BrowseAdmin(admin.ModelAdmin):
    list_display = ('url', 'mode', 'status', 'apply_time', 'create_time')
    search_fields = ('url', )
    list_filter = ('mode', 'status')

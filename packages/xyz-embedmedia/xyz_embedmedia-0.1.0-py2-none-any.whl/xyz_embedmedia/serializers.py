# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from xyz_restful.mixins import IDAndStrFieldSerializerMixin
from rest_framework import serializers
from . import models



class VendorSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        exclude = ()


class ResourceSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.__str__', label=models.Vendor._meta.verbose_name,
                                        read_only=True)

    class Meta:
        model = models.Resource
        exclude = ()

class BrowseSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Browse
        exclude = ()

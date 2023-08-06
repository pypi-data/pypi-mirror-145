# -*- coding:utf-8 -*-
from __future__ import division
from xyz_restful.mixins import BatchActionMixin
from . import models, serializers, vendor, choices
from rest_framework import viewsets, decorators, response
from xyz_restful.decorators import register
from django.conf import settings
from datetime import datetime

@register()
class VendorViewSet(BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    search_fields = ('name',)
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact']
    }

@register()
class ResourceViewSet(BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    search_fields = ('name',)
    filter_fields = {
        'id': ['in', 'exact'],
        'status': ['exact']
    }


    @decorators.action(['GET'], detail=False)
    def explain(self, request):
        ps = request.query_params
        qd = dict(ps.items())
        url = qd.pop('url')
        r = response.Response(vendor.explain(url, proxy=True, **qd))
        aos = getattr(settings, 'ALLOW_ORIGINS', [])
        origin = request.META.get('HTTP_ORIGIN')
        if origin in aos:
            r["Access-Control-Allow-Origin"] = origin
        return r


    @decorators.action(['GET'], detail=False)
    def batch_explain(self, request):
        from . import helper
        c = helper.batch_explain(request.query_params)
        return response.Response({'count': c})


@register()
class BrowseViewSet(BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Browse.objects.all()
    serializer_class = serializers.BrowseSerializer
    search_fields = ('name',)
    filter_fields = {
        'id': ['in', 'exact'],
        'status': ['exact']
    }


    @decorators.action(['GET', 'PATCH'], detail=False, permission_classes=[])
    def apply(self, request):
        qset = self.filter_queryset(self.get_queryset())
        a = qset.filter(status=choices.TASK_PENDING).first()
        rs = []
        if a:
            a.status = choices.TASK_RUNNING
            a.apply_time = datetime.now()
            a.save()
            rs = [serializers.BrowseSerializer(a).data]
        return response.Response(rs)


    @decorators.action(['PATCH'], detail=True, permission_classes=[])
    def upload(self, request, pk):
        obj = self.get_object()
        obj.embed_url = request.data.get('embed_url')
        obj.finish_time = datetime.now()
        obj.status = choices.TASK_SUCCESS
        obj.save()
        return response.Response(serializers.BrowseSerializer(obj).data)

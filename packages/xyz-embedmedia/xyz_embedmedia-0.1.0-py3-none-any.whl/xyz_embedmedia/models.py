# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from xyz_util.modelutils import JSONField
from datetime import datetime, timedelta
from . import choices


# Create your models here.

class Vendor(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "厂商"

    name = models.CharField("名字", max_length=255, unique=True)
    media_expire_minutes = models.PositiveSmallIntegerField("媒体时效(分钟)", blank=True, default=10)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name

    @property
    def average_expire_minutes(self):
        ls = [t.average_expire_minutes for t in self.testings.all()]  # filter(is_active=True)
        return min(ls) if ls else None


class Testing(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "时效检测"

    vendor = models.ForeignKey(Vendor, verbose_name=Vendor._meta.verbose_name, on_delete=models.PROTECT,
                               related_name='testings')
    url = models.URLField("网址", unique=True)
    name = models.CharField("名字", max_length=255, blank=True, default='')
    embed_url = models.TextField("内嵌网址", blank=True, null=True)
    type = models.CharField("类别", max_length=16, blank=True, null=True)
    explain_time = models.DateTimeField("解释时间", blank=True, null=True)
    expire_time = models.DateTimeField("失效时间", blank=True, null=True)
    expire_minutes = models.PositiveIntegerField("失效分钟数", blank=True, default=10)
    next_time = models.DateTimeField("下次执行时间", blank=True, null=True)
    history = JSONField('历史', blank=True)
    is_active = models.BooleanField('有效', blank=True, default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.history:
            self.history = []
        if not self.name:
            self.name = '-'
        if self.explain_time is None:
            self.explain_time = datetime.now()
        self.next_time = self.cal_next_time()
        return super(Testing, self).save(**kwargs)

    def expires(self):
        lm = self.expire_minutes = self.last_minutes
        self.history = ([lm] + self.history)[:10]
        if len(self.history) >= 10:
            self.is_active = False
        self.expire_time = datetime.now()
        self.expire_minutes = self.last_minutes
        self.embed_url = None

    @property
    def last_minutes(self):
        return int((
                               self.update_time - self.explain_time).total_seconds() / 60) if self.update_time and self.explain_time else 0

    @property
    def average_expire_minutes(self):
        return int(sum(self.history) / len(self.history)) if self.history else self.last_minutes

    def cal_next_time(self):
        wm = 60 * 24 * 7
        aem = self.average_expire_minutes
        if not self.embed_url:
            nm = 1
        elif aem > wm:
            nm = wm
        elif len(self.history) >= 10 and abs(self.last_minutes - self.average_expire_minutes) < (
                self.average_expire_minutes / 2):
            nm = 60 * 24
        else:
            nm = max(5, self.average_expire_minutes / 2)
        return datetime.now() + timedelta(minutes=nm)

    def run(self):
        from .helper import run_vendor_testing
        run_vendor_testing(self)


class Resource(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "资源"

    url = models.URLField('网址', max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, verbose_name=Vendor._meta.verbose_name, blank=True, null=True,
                               on_delete=models.PROTECT, related_name='resources')
    name = models.CharField('名称', max_length=255, blank=True, db_index=True)
    embed_url = models.TextField('媒体网址', blank=True, null=True)
    cover = models.URLField('封面', max_length=255, blank=True, null=True)
    width = models.PositiveSmallIntegerField('宽度', blank=True, null=True)
    height = models.PositiveSmallIntegerField('高度', blank=True, null=True)
    duration = models.PositiveSmallIntegerField('时长', blank=True, null=True)
    orientation = models.PositiveSmallIntegerField('横竖', blank=True, null=True, choices=choices.CHOICES_ORIENTATION)
    like_count = models.PositiveIntegerField('点赞数', blank=True, null=True)
    media_type = models.PositiveSmallIntegerField('类型', blank=True, null=True, choices=choices.CHOICES_MEDIA)
    unique_id = models.CharField('排重ID', max_length=32, blank=True, null=True, db_index=True)
    author_name = models.CharField('作者名称', max_length=64, blank=True, null=True)
    status = models.PositiveSmallIntegerField('状态', blank=True, null=True, choices=choices.CHOICES_STATUS,
                                              default=choices.STATUS_READY, db_index=True)
    publish_time = models.DateTimeField('发布时间', null=True, blank=True, db_index=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)
    expire_time = models.DateTimeField('失效时间', null=True, blank=True)

    def __str__(self):
        return self.name or self.url

    def save(self, **kwargs):
        if self.cover:
            self.cover = self.cover[:255]
        super(Resource, self).save(**kwargs)

    def explain(self, proxy=True):
        from .vendor import explain
        return explain(self.url, proxy=proxy)

    def crawl(self, proxy=True, force_update=False):
        now = datetime.now()
        if not self.embed_url \
                or not self.like_count \
                or len(self.embed_url) >= 255 \
                or self.expire_time is None \
                or self.expire_time < now \
                or force_update:
            from . import helper
            vd = self.explain(proxy=proxy)
            if vd and vd.get('status') == 'source_vanish':
                self.status = choices.STATUS_VANISH
                self.save()
            elif vd and vd.get('embed_url'):
                d = helper.explain_resource_fields(vd)
                for k, v in d.items():
                    setattr(self, k, v)
                if d.get('unique_id'):
                    vendor = d.get('vendor')
                    p = vendor.resources.filter(unique_id=d.get('unique_id')) \
                        .exclude(id=self.id) \
                        .exclude(status=choices.STATUS_DUPLICATE).first()
                    if p:
                        self.status = choices.STATUS_DUPLICATE
                self.save()
                helper.save_resource_longtxt(self, vd)
                return vd.get('embed_url')  # 表字段要省空间只存255字符以内的url，这里返回原值，临时用一下
            else:
                # self.is_active = False
                self.embed_url = None
                self.status = choices.STATUS_SOURCE_INVALID
                self.save()
        return self.embed_url


class LongText(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "长文"

    resource = models.OneToOneField(Resource, verbose_name=Resource._meta.verbose_name, on_delete=models.PROTECT)
    content = models.TextField('内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.resource.name


class Browse(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "浏览"

    url = models.URLField('网址', max_length=255, unique=True)
    status = models.PositiveSmallIntegerField('状态', blank=True, default=choices.TASK_PENDING,
                                              choices=choices.CHOICES_TASK)
    mode = models.PositiveSmallIntegerField('模式', blank=True, default=choices.MODE_PC,
                                              choices=choices.CHOICES_MODE)
    script = models.TextField('脚本', blank=True, default='')
    embed_url = models.TextField('媒体网址', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)
    apply_time = models.DateTimeField('申请时间', blank=True, null=True)
    finish_time = models.DateTimeField('结束时间', blank=True, null=True)

    def __str__(self):
        return self.url

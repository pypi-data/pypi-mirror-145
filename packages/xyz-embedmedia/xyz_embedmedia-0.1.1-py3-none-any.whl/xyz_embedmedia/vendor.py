# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals, print_function
from six import string_types
try:
    from urllib.parse import urljoin, urlsplit
except:
    from urlparse import urljoin, urlsplit

from .helper import ScrapyResponse, extract_url, ensure_url_schema, get_redirect_url, UA_MOBILE, is_m3u8, \
    get_m3u8_parts, \
    trim_text
import re, requests, time
import logging
from datetime import datetime, timedelta

log = logging.getLogger('django')

_REGISTER = {}
_SHORTURL_MAP = {}


def register(vendor_class):
    v = vendor_class()
    if v.name in _REGISTER:
        raise Exception('%s has already in vendor register.' % v.name)
    _REGISTER[v.name] = vendor_class
    if v.shorturl_domain:
        _SHORTURL_MAP[v.shorturl_domain] = v


class Cache(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def __getitem__(self, item):
        if not self.prefix:
            return None
        from django.core.cache import cache
        return cache.get(self.prefix + '.' + item)

    def __setitem__(self, key, value):
        if not self.prefix:
            return
        from django.core.cache import cache
        return cache.set(self.prefix + '.' + key, value)


def get_vendor(name):
    return _REGISTER[name]()


def is_short_url(url):
    ps = urlsplit(url)
    sdomain = ps.netloc
    if sdomain in _SHORTURL_MAP:
        return get_redirect_url(url)


class Vendor(object):
    name = ''
    sub_domains = None
    test_urls = []
    icon = None
    type = None
    image_resize = None
    shorturl_domain = None

    def __init__(self, proxy=False):
        from . import CACHE_PREFIX_VENDOR
        self.proxy = proxy
        self.data = {}
        prefix = (CACHE_PREFIX_VENDOR + self.name) if self.name else None
        self.cache = Cache(prefix)

    def explain(self, url):
        ps = urlsplit(url)
        sdomain = ps.netloc
        if sdomain == self.shorturl_domain:
            url = get_redirect_url(url)
            ps = urlsplit(url)
            sdomain = ps.netloc
        f = self.route(sdomain)
        if f:
            response = self.get_response(url, f)
            f(response)
            self.normalize(url)
            return self.data

    def get_response(self, url, explain_func=None):
        d = self.request_extra_params(explain_func)
        return ScrapyResponse(url, **d)

    def request_extra_params(self, f):
        d = dict(proxy=self.proxy)
        return d

    def get_expire_minute(self):
        vem = self.cache['EM']
        if vem is None:
            from .models import Vendor
            v = Vendor.objects.filter(name=self.name).first()
            if v:
                vem = v.average_expire_minutes
            self.cache['EM'] = vem
        return vem

    def source_vanish(self):
        # self.data['source_vanish'] = True
        raise LookupError('VANISH')

    def normalize(self, url):
        d = self.data
        if not d:
            return
        d.update(dict(vendor=self.name, url=url))
        d['type'] = d.get('embed_url') and d.get('type') or 'normal'
        for a in ['cover', 'embed_url', 'icon']:
            if a in d:
                d[a] = ensure_url_schema(d[a])
        if self.image_resize and d.get('cover'):  # and d['type'] == 'audio'
            d['cover'] += self.image_resize
        if not d.get('expire_time'):
            d['expire_time'] = self.get_expire_time()
        for a in ['name', 'content', 'description']:
            if d.get(a):
                d[a] = trim_text(d[a])

    def get_expire_time(self):
        em = self.get_expire_minute()
        if em:
            return int(time.mktime((datetime.now() + timedelta(minutes=em)).timetuple())) * 1000

    def route(self, sub_domain):
        for k, n in self.get_sub_domains().items():
            r = re.compile(k)
            if r.search(sub_domain):
                return getattr(self, 'explain_%s' % n)

    def get_sub_domains(self):
        sub_domains = self.sub_domains
        if isinstance(sub_domains, string_types):
            sub_domains = {sub_domains: 'default'}
        elif isinstance(sub_domains, (tuple, list)):
            sub_domains = dict([(a, 'default') for a in sub_domains])
        return sub_domains

    def get_icon(self, response=None):
        icon = self.icon or self.cache['icon']
        if icon:
            return icon
        if not response:
            dm = list(self.get_sub_domains().keys())[0]
            if len(dm.split('.')) == 2:
                dm = "www.%s" % dm
            response = self.get_response('http://%s' % dm)
        url = '/favicon.ico'
        for p in ['rel="icon"', 'rel="shortcut icon"', 'type="image/x-icon"']:
            a = response.css('link[%s]::attr(href)' % p).get()
            if a and not a.endswith('.svg'):
                url = a
                break
        url = self.normalize_url(response, url)
        try:
            r = self.get_response(url)
            if r.status == 200:
                icon = r.url
                self.cache['icon'] = icon
                return icon
        except:
            return None

    def normalize_url(self, response, url):
        if url and url[0] == '/' and url[1] != '/':
            p = response.css('head base::attr(href)').get() or response.url
            return urljoin(p, url)
        if url.startswith('//'):
            url = 'https:%s' % url
        return url

    def get_name(self, response):
        name = response.css('meta[property="og:title"]::attr("content")').get() \
               or response.css('meta[itemprop="name"]::attr("content")').get() \
               or response.css('title::text').get()
        return name and name.strip()

    def get_cover(self, response):
        for p in ['meta[property="og:image"]::attr("content")',
                  'meta[itemprop="image"]::attr("content")',
                  'img[src*="logo"]::attr(src)',
                  'link[rel="apple-touch-icon"]::attr(href)']:
            url = response.css(p).get()
            if url and not url.endswith('.svg'):
                return self.normalize_url(response, url)

    def get_description(self, response):
        description = response.css('meta[property="og:description"]::attr("content")').get() \
                      or response.css('meta[itemprop="description"]::attr("content")').get() \
                      or response.css('meta[name="description"]::attr("content")').get()
        return description

    def get_type(self, response):
        type = self.type or response.css('meta[property="og:type"]::attr("content")').get() or 'normal'
        return type

    def explain_default(self, response):
        d = self.data
        d['name'] = self.get_name(response)
        d['description'] = self.get_description(response)
        d['cover'] = self.get_cover(response)
        d['type'] = self.get_type(response)
        d['icon'] = self.get_icon(response)
        d['page_url'] = response.url

    def explain_shorturl(self, response):
        for k, v in self.sub_domains.items():
            if v == 'shorturl':
                continue
            if k in response.url:
                func = getattr(self, 'explain_%s' % v)
                return func(response)
        return self.explain_default(response)

    def get_list_functions(self):
        return [getattr(self, fn) for fn in dir(self) if fn.startswith('list_') and callable(getattr(self, fn))]

    def match_url(self, url, func_name=None):
        if func_name:
            func = getattr(self, func_name)
            if func and hasattr(func, 'url_patterns'):
                funcs = [func]
            else:
                return
        else:
            funcs = self.get_list_functions()
        for func in funcs:
            for pattern in getattr(func, 'url_patterns', []):
                m = re.search(pattern, url)
                if m:
                    return dict(match=m, function=func)

    def extract_user_info(self, url, func):
        pass

    def extract_list_cover(self, url, func):
        pass


class DefaultVendor(Vendor):
    sub_domains = '.*'
    proxy_except_list = ['mp.weixin.qq.com']

    def get_response(self, url, explain_func=None):
        for a in self.proxy_except_list:
            if a in url:
                return ScrapyResponse(url, proxy=False)
        return super(DefaultVendor, self).get_response(url, explain_func=explain_func)


def register_all():
    import importlib
    from django.conf import settings

    for pkg, mns in settings.EMBEDMEDIA_VENDORS:
        for mn in mns:
            md = importlib.import_module('%s.%s' % (pkg, mn))


register_all()


def explain(s, proxy=False, **kwargs):
    url = extract_url(s)
    if not url:
        return None
    vs = _REGISTER
    for k, vc in list(vs.items()) + [('', DefaultVendor)]:
        v = vc()
        v.proxy = proxy
        for k, vl in kwargs.items():
            setattr(v, k, vl)
        try:
            d = v.explain(url)
            if not d:
                continue
        except requests.exceptions.ProxyError as e:
            return dict(status='proxy_error')
        except LookupError as e:
            if e.args[0] == 'VANISH':
                return dict(status='source_vanish')
        except:
            import traceback
            log.error('embedmedia.vendor.explain "%s" error: %s', s, traceback.format_exc())
            continue
        if d:
            return d


# def test_all():
#     for k, vc in _REGISTER.items():
#         try:
#             test_vendor(vc)
#         except Exception:
#             import traceback
#             log.error('test_vendor %s error: %s', k, traceback.format_exc())
#
#
# def test_vendor(vendor):
#     from .models import Item
#     from datetime import datetime
#     from time import sleep
#     for url in vendor.test_urls:
#         print(vendor.name, url)
#         v = vendor()
#         item, created = Item.objects.get_or_create(
#             url=url,
#             defaults=dict(
#                 name='',
#                 vendor=v.name
#             )
#         )
#         if not item.embed_url:
#             v.explain(url)
#             item.explain_time = datetime.now()
#             item.embed_url = v.data['embed_url']
#             if not item.embed_url:
#                 log.error('test_vendor %s %s 取不到媒体地址.', v, url)
#                 break
#             item.cover = v.data['cover']
#             item.name = v.data['name']
#             item.type = v.data['type']
#             item.detail = v.data.get('detail')
#             item.save()
#         if not item.explain_time:
#             item.explain_time = item.create_time
#         flag = False
#         try:
#             r = requests.get(item.embed_url, headers={'User-Agent': UA_MOBILE}, timeout=(5, 5), stream=True)
#             if r.status_code == 200:
#                 if is_m3u8(r):
#                     ps = get_m3u8_parts(r.text)
#                     if ps:
#                         r = requests.get(urljoin(item.embed_url, ps[0]), headers={'User-Agent': UA_MOBILE},
#                                          timeout=(5, 5), stream=True)
#                         if r.status_code == 200:
#                             flag = True
#                 else:
#                     flag = True
#         except:
#             import traceback
#             log.error('test_vendor %s error: %s', vendor, traceback.format_exc())
#         if not flag:
#             item.expire_time = datetime.now()
#             item.embed_url = None
#         item.last_minutes = (item.modify_time - item.explain_time).seconds / 60
#         item.save()
#         print(item.id, item.last_minutes)
#         sleep(3)

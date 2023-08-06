# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals, print_function
from . import choices, models
import logging, json

try:
    from urllib.parse import urljoin, urlsplit, urlencode
except:
    from urlparse import urljoin, urlsplit, urlencode


log = logging.getLogger('django')

from xyz_util.crawlutils import *

def wrap_h5player(url):
    return 'http://quiz.iuse.xyz/static/video.html?' + url


def batch_explain(ps):
    from . import vendor
    from time import sleep
    url = ps.get('url')
    v = vendor.get_vendor(ps['vendor'])
    v.proxy = True
    f = getattr(v, 'explain_%s' % ps['func'])
    rs = []
    from crawlstore.models import Domain
    domain, created = Domain.objects.get_or_create(name=ps['vendor'])
    category, created = domain.categories.update_or_create(domain=domain, name=ps['category'])
    c = 0
    icon = v.get_icon()
    for d in f(v.get_response(url), pages=ps.get('pages', [])):
        al = d['data']
        for a in al:
            di = dict(vendor=v.name, icon=icon, type='video')
            di.update(a)
            item, created = category.items.update_or_create(url=di['url'],
                                                            defaults=dict(content_json=di, name=di['name']))
            rs.append(item.url)
            # print item.url
        c += len(al)
        sleep(3)
    return c


def get_m3u8_parts(s):
    rs = []
    for l in s.split('\n'):
        l = l.strip()
        if not l or l.startswith('#'):
            continue
        rs.append(l)
    return rs


def is_m3u8(r):
    hs = r.headers
    if 'vnd.apple.mpegurl' in hs['Content-Type']:
        return True
    return False


def load_vendors_into_db():
    from . import vendor, models
    for vn, vc in vendor._REGISTER.items():
        vm, created = models.Vendor.objects.get_or_create(name=vn)
        for url in vc.test_urls:
            tm, created = vm.testings.get_or_create(url=url)
            print(vm, tm.url)


def run_vendor_testing(testing):
    from .vendor import get_vendor
    v = get_vendor(testing.vendor.name)
    v.proxy = True
    t = testing
    if not t.embed_url:
        v.explain(t.url)
        t.explain_time = datetime.now()
        t.embed_url = v.data['embed_url']
        t.type = v.data['type']
        t.name = v.data['name']
        t.save()
    if not t.embed_url:
        log.error('test_vendor %s %s 取不到媒体地址.', v, t.url)
    flag = False
    try:
        r = requests.get(t.embed_url, headers={'User-Agent': UA_MOBILE}, timeout=(5, 5), stream=True)
        if r.status_code == 200:
            if is_m3u8(r):
                ps = get_m3u8_parts(r.text)
                if ps:
                    r = requests.get(urljoin(t.embed_url, ps[0]), headers={'User-Agent': UA_MOBILE}, timeout=(5, 5),
                                     stream=True)
                    if r.status_code == 200:
                        flag = True
            else:
                flag = True
    except:
        import traceback
        log.error('test_vendor %s error: %s', v, traceback.format_exc())
    if not flag:
        t.expires()
    t.save()


def html2text(text):
    return re.sub('<.*?>', '', text, flags=re.M | re.S) \
        .replace('&quot;', '"') \
        .replace('&copy;', '©') \
        .replace('&lt;', '<') \
        .replace('&gt;', '>') \
        .replace('&amp;', '&') \
        .replace('&#39;', "'") \
        .replace('&apos;', "'")


def firefox_get(url):
    from selenium import webdriver
    page = webdriver.Firefox()
    page.get(url)
    text = page.page_source
    page.close()
    return text


def explain_resource_fields(d):
    vendor = models.Vendor.objects.get(name=d.get('vendor'))
    rd = dict(
        vendor=vendor,
        name=trim_text(d['name'])[:255],
        embed_url=d['embed_url'] if 'embed_url' in d else None,
        cover=d.get('cover'),
        media_type=choices.MEDIA_VIDEO if d['type'] == 'video' else choices.MEDIA_AUDIO,
        width=d.get('width'),
        height=d.get('height'),
        duration=int(float(d.get('duration'))) if d.get('duration') else None,
        orientation=d.get('orientation'),
        expire_time=datetime.fromtimestamp(d['expire_time'] / 1000) if d.get('expire_time') else None,
        like_count=d.get('like_count'),
        unique_id=d.get('unique_id'),
        author_name=d.get('author_name')
    )

    if d.get('orientation') == 'horizontal':
        rd['orientation'] = choices.ORIENTATION_HORIZONTAL
    elif d.get('orientation') == 'vertical':
        rd['orientation'] = choices.ORIENTATION_VERTICAL

    if d.get('publish_time'):  # 存在内容页比列表页字段少的情况，这里要避免把数据又置空了。
        rd['publish_time'] = datetime.fromtimestamp(d['publish_time'] / 1000)
    return rd


def save_resource(d):
    rd = explain_resource_fields(d)
    rd['url'] = d['url'][:255]
    vendor = rd['vendor']
    uid = rd.get('unique_id')
    r = None
    if uid:
        uid = str(uid)
        r = vendor.resources.filter(unique_id=uid).first()
        if r:
            ouid = r.unique_id
            r.unique_id = md5(ouid)
            r.expire_time = rd['expire_time']
            r.like_count = rd.get('like_count') or r.like_count
            r.save()
            if ouid == uid:
                return r
        else:
            r = vendor.resources.filter(unique_id=md5(uid)).first()
            if r:
                r.expire_time = rd['expire_time']
                r.like_count = rd.get('like_count') or r.like_count
                r.save()
                return r
        rd['unique_id'] = md5(uid)
    if not r:
        r = vendor.resources.filter(url=rd['url']).first()
        if r:
            r.expire_time = rd['expire_time']
            r.like_count = rd.get('like_count') or r.like_count
            r.save()
            return r
    r = models.Resource(**rd)
    r.save()
    save_resource_longtxt(r, d)
    return r

def explain_and_save_resouce(url):
    from .vendor import explain
    d = explain(url)
    return save_resource(d)

def save_resource_longtxt(r, d):
    if 'content' in d:
        models.LongText.objects.get_or_create(
            resource=r,
            defaults=dict(
                content=d['content']
            )
        )

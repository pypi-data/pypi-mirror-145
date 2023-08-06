# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import print_function, unicode_literals
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
import requests, argparse, codecs
from collections import OrderedDict


def get_args():
    parser = argparse.ArgumentParser(description="媒体浏览")
    parser.add_argument('-t', '--token', default='')
    parser.add_argument('-e', '--endpoint', default='https://oss.drfun.cn/api/embedmedia/browse')
    return parser.parse_args()


def retry(func, times=3):
    try:
        return func()
    except:
        if times > 1:
            return retry(func, times - 1)
        return '重试失败'


def element(driver, css):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))


def str2dict(s, line_spliter='\n', key_spliter=':'):
    d = OrderedDict()
    s = s.strip()
    if not s:
        return d
    for a in s.split(line_spliter):
        a = a.strip()
        if not a:
            continue
        p = a.find(key_spliter)
        if p == -1:
            d[a] = ""
        else:
            d[a[:p].strip()] = a[p + 1:].strip()
    return d


MOBILE_EMULATION = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},  # 定义设备高宽，像素比
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "  # 通过UA来模拟
                 "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
}


def browse_to_get_media_src(url, script=None, mobile_mode=False):
    def video_url():
        return element(driver, "video").get_attribute('src')

    if not script:
        script = 'video_url()'

    options = webdriver.ChromeOptions()
    if mobile_mode:
        options.add_experimental_option('mobileEmulation', MOBILE_EMULATION)
    driver = webdriver.Chrome(options=options)
    rs = None
    try:
        driver.get(url)
        for s in script.split('\n'):
            s = s.strip()
            if not s:
                continue
            rs = eval(s)
    finally:
        driver.close()
    return rs


def run_browse_task(endpoint, headers={}):
    r = requests.get('%s/apply/' % endpoint, headers=headers)
    rs = r.json()
    if r.status_code != 200:
        print(rs['detail'])
        return
    if rs:
        task = rs[0]
        embed_url = browse_to_get_media_src(task['url'], task['script'], mobile_mode=task['mode'] == 2)
        r = requests.patch('%s/%d/upload/' % (endpoint, task['id']), dict(embed_url=embed_url), headers=headers)
        return r.json()


if __name__ == '__main__':
    args = get_args()
    headers = {'Authorization': 'Token %s' % args.token}
    endpoint = args.endpoint
    while True:
        try:
            r = run_browse_task(endpoint, headers=headers)
            if not r:
                print('no more, wait...')
                sleep(10)
            else:
                print('success', r['url'], r['finish_time'])
        except:
            import traceback

            traceback.print_exc()
            sleep(10)
        sleep(1)

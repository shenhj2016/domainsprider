# -*- coding:utf-8 -*-
import sys
import ssl
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')


def testhttp():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    context = ssl._create_unverified_context()
    # 以下三段设置代理
    proxy_s = urllib2.ProxyHandler({"http": "http://36.48.73.16:80"})
    opener = urllib2.build_opener(proxy_s)
    urllib2.install_opener(opener)
    request = urllib2.Request("http://shenhj.frp.ngarihealth.com/welcome", headers=headers)
    # 3. 在urlopen()方法里 指明添加 context 参数
    response = urllib2.urlopen(request, context=context)
    res = response.read()
    print res


if __name__ == '__main__':
    testhttp()
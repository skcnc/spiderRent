#!/usr/bin/env python
# -*- coding:utf8 -*-
from GRFY.Crawler import *
from ANJUKESOURCE.Crawler import *
from WUBATONGCHENG.Crawler import *
from GANJI.Crawler import *
from SOUFANG.Crawler import *
from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
from Utils.Opener import *
import time
import chardet
from StringIO import StringIO
import gzip

try:
    #模拟登陆至房探主页
    init()
    url = 'http://zu.sh.fang.com/chuzu/1_53924434_-1.htm'
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = unicode(f.read(),'gbk').encode('utf8')
        data = re.sub('\<script[\S|\s]+?script\>','',data)
        bsObj = BeautifulSoup(data)
    ul = bsObj.findAll("ul",{"class","house-info"})[0]
    for ele in ul.contents:
        print(ele.text)
except Exception,ex:
    print(ex)

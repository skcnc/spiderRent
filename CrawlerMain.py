# -*- coding: utf-8 -*-
from GRFY.Crawler import *
from ANJUKESOURCE.Crawler import *
from WUBATONGCHENG.Crawler import *
from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
from Utils.Opener import *
import time

try:
    #模拟登陆至房探主页
    init()
    WUBA = WUBATONGCHENG(1)
    WUBA.crawler("http://sh.fangtan007.com/chuzu/fangwu/w01/")
except Exception,ex:
    print(ex)

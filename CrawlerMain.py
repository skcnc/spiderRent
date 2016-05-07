# -*- coding: utf-8 -*-
from GRFY.Crawler import *
from ANJUKESOURCE.Crawler import *
from WUBATONGCHENG.Crawler import *
from GANJI.Crawler import *
from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
from Utils.Opener import *
import time

try:
    #模拟登陆至房探主页
    init()
    GANJI_thread = GANJI(1)
    #GANJI_thread.crawler("http://sh.fangtan007.com/chuzu/fangwu/w02/")
    GANJI_thread.crawler_level2("http://sh.fangtan007.com/fangwu/7295753.html")
except Exception,ex:
    print(ex)

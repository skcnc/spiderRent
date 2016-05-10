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
from FOCUSCN.Crawler import *
from FIRSTFYCN.Crawler import *


try:
    #模拟登陆至房探主页
    init()
    SOUFANG_thread  = SOUFANG(1)
    SOUFANG_thread.crawler()
    #SOUFANG_thread.crawler_level2("http://sh.fangtan007.com/fangwu/7306732.html")
except Exception,ex:
    print(ex)

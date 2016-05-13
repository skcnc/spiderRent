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
from FOCUSCN.Crawler import *
from FIRSTFYCN.Crawler import *


try:
    #模拟登陆至房探主页
    init()
    #GRFY_thread = GRFY(6)
    #GRFY_thread.crawler_level2("d-11988407.html")
    # time.sleep(5)
    # SOUFANG_thread  = SOUFANG(1)
    # SOUFANG_thread.start()
    # time.sleep(5)
    #ANJUKE_thread = ANJUKE(2)
    #ANJUKE_thread.crawler_level2("http://sh.zu.anjuke.com/gfangyuan/69512100")
    # time.sleep(5)
    #FIRSTFYCN_thread = FIRSTFYCN(3)
    #FIRSTFYCN_thread.crawler_level2("")
    # time.sleep(5)
    #FOCUSCN_thread = FOCUSCN(4)
    #FOCUSCN_thread.crawler_level2("http://sh.fangtan007.com/fangwu/7115416.html")
    # time.sleep(5)
    GANJI_thread = GANJI(5)
    GANJI_thread.crawler_level2("http://sh.fangtan007.com/fangwu/7332207.html")
    # time.sleep(5)
    # WUBATONGCHENG_thread = WUBATONGCHENG(7)
    # WUBATONGCHENG_thread.start()
    # time.sleep(5)
    quit = False
    while quit == False:
        time.sleep(1000)
except Exception,ex:
    # SOUFANG_thread.stop()
    # ANJUKE_thread.stop()
    # FIRSTFYCN_thread.stop()
    # FOCUSCN_thread.stop()
    # GANJI_thread.stop()
    # GRFY_thread.stop()
    # WUBATONGCHENG_thread.stop()
    print(ex)
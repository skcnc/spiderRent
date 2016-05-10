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
    time.sleep(5)
    ANJUKE_thread = ANJUKE(2)
    time.sleep(5)
    FIRSTFYCN_thread = FIRSTFYCN(3)
    time.sleep(5)
    FOCUSCN_thread = FOCUSCN(4)
    time.sleep(5)
    GANJI_thread = GANJI(5)
    time.sleep(5)
    GRFY_thread = GRFY(6)
    time.sleep(5)
    WUBATONGCHENG = GRFY(7)
    time.sleep(5)
    quit = False
    while quit == False:
        time.sleep(1000)
except Exception,ex:
    print(ex)

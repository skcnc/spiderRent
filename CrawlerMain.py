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


try:
    #模拟登陆至房探主页
    init()
    Sqlite = SqliteOpenClass()
    r =  Sqlite.getestatelinkwithname('幸福小镇')
    print(r[0])
    #SOUFANG_thread  = SOUFANG(1)
    #SOUFANG_thread.crawler()
except Exception,ex:
    print(ex)

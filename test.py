#!/usr/bin/env python
# -*- coding:utf8 -*-
from GANJI.Crawler import *
from Utils.Opener import *
from FOCUSCN.Crawler import *

init()
#GANJI_thread = GANJI(5)
#GANJI_thread.crawler_level2("http://sh.fangtan007.com/fangwu/7448378.html")

ANJUKE_thread = FOCUSCN(2)
ANJUKE_thread.start()
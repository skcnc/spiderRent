#!/usr/bin/env python
# -*- coding:utf8 -*-
from GRFY.Crawler import *
from ANJUKESOURCE.Crawler import *
from WUBATONGCHENG.Crawler import *
from GANJI.Crawler import *
from SOUFANG.Crawler import *
from FOCUSCN.Crawler import *
from FIRSTFYCN.Crawler import *



quit = False
while quit == False:
    try:
    #模拟登陆至房探主页
        init()
        GRFY_thread = GRFY(6)
        GRFY_thread.start()
        time.sleep(5)
        SOUFANG_thread  = SOUFANG(1)
        SOUFANG_thread.start()
        time.sleep(5)
        ANJUKE_thread = ANJUKE(2)
        ANJUKE_thread.start()
        time.sleep(5)
        FIRSTFYCN_thread = FIRSTFYCN(3)
        FIRSTFYCN_thread.start()
        time.sleep(5)
        FOCUSCN_thread = FOCUSCN(4)
        FOCUSCN_thread.start()
        time.sleep(5)
        GANJI_thread = GANJI(5)
        GANJI_thread.start()
        time.sleep(5)
        WUBATONGCHENG_thread = WUBATONGCHENG(7)
        WUBATONGCHENG_thread.start()
        time.sleep(5)
    except Exception,ex:
        print("执行结束！")
        pass
    time.sleep(6000)
    Sql =SqliteOpenClass()
    Sql.movehousedata()
    SOUFANG_thread.stop()
    ANJUKE_thread.stop()
    FIRSTFYCN_thread.stop()
    FOCUSCN_thread.stop()
    GANJI_thread.stop()
    GRFY_thread.stop()
    WUBATONGCHENG_thread.stop()
    time.sleep(70)
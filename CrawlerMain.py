#!/usr/bin/env python
# -*- coding:utf8 -*-
from GRFY.Crawler import *
from ANJUKESOURCE.Crawler import *
from WUBATONGCHENG.Crawler import *
from GANJI.Crawler import *
from SOUFANG.Crawler_2 import *
from FOCUSCN.Crawler import *
from FIRSTFYCN.Crawler import *
from Utils.SMTP import *


quit = False
GRFYURL = ''
SOUFANGURL = ''
ANJUKEURL = ''
FIRSTFYCNURL = ''
FOCUSCNURL = ''
GANJIURL = ''
WUBATONGCHENGURL = ''
while quit == False:
    try:
    #模拟登陆至房探主页
        init()
        initPhonelady()
        GRFY_thread = GRFY(6)
        GRFY_thread.LastUrl = GRFYURL
        GRFY_thread.start()
        time.sleep(5)
        SOUFANG_thread  = SOUFANG2(1)
        SOUFANG_thread.LastUrl = SOUFANGURL
        SOUFANG_thread.start()
        time.sleep(5)
        ANJUKE_thread = ANJUKE(2)
        ANJUKE_thread.LastUrl = ANJUKEURL
        ANJUKE_thread.start()
        time.sleep(5)
        FIRSTFYCN_thread = FIRSTFYCN(3)
        FIRSTFYCN_thread.LastUrl = FIRSTFYCNURL
        FIRSTFYCN_thread.start()
        time.sleep(5)
        FOCUSCN_thread = FOCUSCN(4)
        FOCUSCN_thread.LastUrl = FOCUSCNURL
        FOCUSCN_thread.start()
        time.sleep(5)
        GANJI_thread = GANJI(5)
        GANJI_thread.LastUrl = GANJIURL
        GANJI_thread.start()
        time.sleep(5)
        WUBATONGCHENG_thread = WUBATONGCHENG(7)
        WUBATONGCHENG_thread.LastUrl = WUBATONGCHENGURL
        WUBATONGCHENG_thread.start()
        time.sleep(5)
    except Exception,ex:
        print(ex)
        sendmail(ex)
        pass

    time.sleep(6000)
    print(str(ANJUKE_thread.isAlive()) + "|" + str(FIRSTFYCN_thread.isAlive()) + "|" + str(FOCUSCN_thread.isAlive()) + "|" + str(GANJI_thread.isAlive()) + "|" + str(GRFY_thread.isAlive()) + "|" + str(SOUFANG_thread.isAlive()) + "|" + str(WUBATONGCHENG_thread.isAlive()))
    sql = SqliteOpenClass()
    sendmail("检索状态：\n\r\t安居客：" + str(ANJUKE_thread.isAlive()) + "\r\n\t第一房源：" + str(FIRSTFYCN_thread.isAlive()) + "\r\n\t焦点房产：" + str(FOCUSCN_thread.isAlive()) + "\r\n\t赶集网：" + str(GANJI_thread.isAlive())
            +  "\r\n\tGRFY：" +  str(GRFY_thread.isAlive()) + "\r\n\t搜房网：" + str(SOUFANG_thread.isAlive()) + "\r\n\t58同城：" + str(WUBATONGCHENG_thread.isAlive()) + "\r\n"
            +  "上次循环获取房源总计："
            + str(sql.getcurrentnum()) + " /" + str(ANJUKE_thread.highcount + FIRSTFYCN_thread.highcount
                                                    + GANJI_thread.highcount + FOCUSCN_thread.highcount + GRFY_thread.highcount + SOUFANG_thread.highcount + WUBATONGCHENG_thread.highcount)
            + "\r\n\r\n"
            +  "其中： \r\n\r\n"
            +  "安居客：" + str(ANJUKE_thread.count) + " /" + str(ANJUKE_thread.highcount) + "\r\n"
            +  "第一房源："  + str(FIRSTFYCN_thread.count) + " /" + str(FIRSTFYCN_thread.highcount) + "\r\n"
            +  "焦点房产：" + str(FOCUSCN_thread.count) + " /" + str(FOCUSCN_thread.highcount) + "\r\n"
            +  "赶集网：" + str(GANJI_thread.count) +" /" + str(GANJI_thread.highcount) +  "\r\n"
            +  "GRFY：" + str(GRFY_thread.count) + " /" + str(GRFY_thread.highcount) + "\r\n"
            +  "搜房网：" + str(SOUFANG_thread.count) +" /" + str(SOUFANG_thread.highcount) +  "\r\n"
            +  "58同城：" + str(WUBATONGCHENG_thread.count) + " /" + str(WUBATONGCHENG_thread.highcount) + "\r\n"
            +  "历史房源总计：" + str(sql.gethisnum()))
    sql.movehousedata()
    SOUFANGURL = SOUFANG_thread.LastUrl
    SOUFANG_thread.stop()
    ANJUKEURL = ANJUKE_thread.LastUrl
    ANJUKE_thread.stop()
    FIRSTFYCNURL = FIRSTFYCN_thread.LastUrl
    FIRSTFYCN_thread.stop()
    FOCUSCNURL = FOCUSCN_thread.LastUrl
    FOCUSCN_thread.stop()
    GANJIURL = GANJI_thread.LastUrl
    GANJI_thread.stop()
    GRFYURL = GRFY_thread.LastUrl
    GRFY_thread.stop()
    WUBATONGCHENGURL = WUBATONGCHENG_thread.LastUrl
    WUBATONGCHENG_thread.stop()
    time.sleep(70)

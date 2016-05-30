#!/usr/bin/env python
# -*- coding:utf8 -*-

import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def Writelog(str):
    "写入日志文件"
    str_date = time.strftime('%Y_%m_%d',time.localtime(time.time()))
    PATH = unicode("F:\\项目文档\\SpiderRent\\LOGS\\",'utf-8')
    file_object = open(PATH + str_date,"a+")
    try:
        file_object.writelines(str)
        file_object.writelines("\r\n")
    except:
        file_object.close()

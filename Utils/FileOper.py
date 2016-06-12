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

def Readlog():
    "读取日志文件"
    PATH = unicode("F:\\项目文档\\SpiderRent\\address.TXT",'utf-8')
    file_object = open(PATH,'r')
    try:
        return file_object.readlines()
    except  Exception,ex:
        print(ex)

def Writeknown(str,name):
    "写入经纬度文件"
    PATH = unicode("F:\\项目文档\\SpiderRent\\" + name,'utf-8')
    file_object = open(PATH,"a+")
    try:
        file_object.writelines(str)
        file_object.writelines("\r\n")
    except:
        file_object.close()

def Readlocations():
    "读取日志文件"
    PATH = unicode("F:\\项目文档\\SpiderRent\\known.txt",'utf-8')
    file_object = open(PATH,'r')
    try:
        return file_object.readlines()
    except  Exception,ex:
        print(ex)



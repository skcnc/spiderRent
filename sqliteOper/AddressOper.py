#-*- coding: UTF-8 -*-
from urllib import urlopen
from urllib import urlencode
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
from Utils.FileOper import *
import re
import json


def gettraffic():
    try:

        locationlist = Readlocations()
        count = 0
        countall = len(locationlist)
        for item in locationlist:
            item = item.replace('\n','').replace('\r','')
            lanAndLon = item.split('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')[1].replace('\t','')
            address = item.split('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')[0].replace('\t','').replace('?','').replace('...','')
            location = {"location":lanAndLon}
            location = urlencode(location)

            #"http://restapi.amap.com/v3/place/around?key=df5d187ecee6c2a7de61b118ec8f7c2d" +location + "&types=150500&offset=4&page=1&extensions=all"
            StartUrl =   "http://restapi.amap.com/v3/place/around?key=7356684624b4e9a5d025491459a93945&" +location + "&types=150500&offset=4&page=1&extensions=all"
            success = "失败"
            try:
                html = urlopen(StartUrl)
                bsObj = BeautifulSoup(html.read())
                jsonvalue = json.loads(bsObj.text)

                if jsonvalue['status'] == '1':
                    subwayA = jsonvalue['pois'][0]["address"]
                    stationA =  jsonvalue['pois'][0]["name"]
                    distanceA =  jsonvalue['pois'][0]["distance"]
                    subwayB = jsonvalue['pois'][1]["address"]
                    stationB =  jsonvalue['pois'][1]["name"]
                    distanceB =  jsonvalue['pois'][1]["distance"]
                    subwayC = jsonvalue['pois'][2]["address"]
                    stationC =  jsonvalue['pois'][2]["name"]
                    distanceC =  jsonvalue['pois'][2]["distance"]
                    subwayD = jsonvalue['pois'][3]["address"]
                    stationD =  jsonvalue['pois'][3]["name"]
                    distanceD =  jsonvalue['pois'][3]["distance"]
                    sql = SqliteOpenClass()
                    sql.insertTrafficTable(address,lanAndLon,subwayA,stationA,distanceA,subwayB,stationB,distanceB,subwayC,stationC,distanceC,subwayD,stationD,distanceD)
                    success = "成功"
                else:
                    Writeknown(lanAndLon,"unknown.txt")
            except:
                Writeknown(lanAndLon,"unknown.txt")
            count += 1
            print("正在处理第" + str(count) + "个，剩余：" + str(countall - count) + "个，地址： " + address + "  结果：" + success)
            time.sleep(0.1)
    except Exception,ex:
        print(ex)

def getlocation():
    try:
        addlist = Readlog()
        count = 0
        countall = len(addlist)

        for address in addlist:
            address = unicode(address,'gbk')

            if  ' ' in address:
                address = address.split(' ')[0]
            if '，' in address:
                address = address.split('，')[0]
            if '、' in address:
                address = address.split('、')[0]

            address = address.replace('\n','').replace(' ','').replace('?','').replace('...','')

            d = {'address':address}

            encodeaddr = urlencode(d)
            StartUrl = 'http://restapi.amap.com/v3/geocode/geo?' + encodeaddr + '&output=json&key=df5d187ecee6c2a7de61b118ec8f7c2d'
            try:
                html = urlopen(StartUrl)
                bsObj = BeautifulSoup(html.read())
                jsonvalue = json.loads(bsObj.text)

                if jsonvalue['status'] == '1':
                    location = jsonvalue['geocodes'][0]['location']
                    Writeknown(address + '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t' + location,"known.txt")
                else:
                    location = 'unknown'
                    Writeknown(address + '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t' + location,"unknown.txt")
            except:
                location = 'unknown'
                Writeknown(address + '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t' + location,"unknown.txt")
            count += 1
            print("已完成："+ str(count) + "\t剩余：" + str(countall - count) + "\t地址：" + address)
            time.sleep(0.1)
    except Exception,ex:
        print(ex)

def getlocation(address):
    "获取特定小区的地址和经纬度"
    if  ' ' in address:
        address = address.split(' ')[0]
    if '，' in address:
        address = address.split('，')[0]
    if '、' in address:
        address = address.split('、')[0]

    address = address.replace('\n','').replace(' ','').replace('?','').replace('...','')

    d = {'address':address}

    encodeaddr = urlencode(d)
    StartUrl = 'http://restapi.amap.com/v3/geocode/geo?' + encodeaddr + '&output=json&key=df5d187ecee6c2a7de61b118ec8f7c2d'
    try:
        html = urlopen(StartUrl)
        bsObj = BeautifulSoup(html.read())
        jsonvalue = json.loads(bsObj.text)
        if jsonvalue['status'] == '1':
            location = jsonvalue['geocodes'][0]['location']
            print("获取经纬度成功!")
        else:
            print("获取经纬度失败!")
            return
    except:
        print("获取经纬度失败!")
        return

    lanAndLon = location
    location = {"location":lanAndLon}
    location = urlencode(location)

    #"http://restapi.amap.com/v3/place/around?key=df5d187ecee6c2a7de61b118ec8f7c2d" +location + "&types=150500&offset=4&page=1&extensions=all"
    StartUrl =   "http://restapi.amap.com/v3/place/around?key=7356684624b4e9a5d025491459a93945&" +location + "&types=150500&offset=4&page=1&extensions=all"
    success = "失败"
    try:
        html = urlopen(StartUrl)
        bsObj = BeautifulSoup(html.read())
        jsonvalue = json.loads(bsObj.text)

        if jsonvalue['status'] == '1':
            subwayA = jsonvalue['pois'][0]["address"]
            stationA =  jsonvalue['pois'][0]["name"]
            distanceA =  jsonvalue['pois'][0]["distance"]
            subwayB = jsonvalue['pois'][1]["address"]
            stationB =  jsonvalue['pois'][1]["name"]
            distanceB =  jsonvalue['pois'][1]["distance"]
            subwayC = jsonvalue['pois'][2]["address"]
            stationC =  jsonvalue['pois'][2]["name"]
            distanceC =  jsonvalue['pois'][2]["distance"]
            subwayD = jsonvalue['pois'][3]["address"]
            stationD =  jsonvalue['pois'][3]["name"]
            distanceD =  jsonvalue['pois'][3]["distance"]
            sql = SqliteOpenClass()
            sql.insertTrafficTable(address,lanAndLon,subwayA,stationA,distanceA,subwayB,stationB,distanceB,subwayC,stationC,distanceC,subwayD,stationD,distanceD)
            success = "成功"
            print("获取交通信息成功！")
        else:
            print("获取交通信息失败！")
    except:
        print("获取交通信息失败！")


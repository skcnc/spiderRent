#-*- coding: UTF-8 -*-
import sqlite3
import uuid
import time
import threading
from sqliteOper.AddressOper import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from Operations import *
from Utils.Opener import *

init()
SearchUrl = '/community/view/2903'
AliasB = ''
AliasC = ''
AliasD = ''
if SearchUrl == '':
     EstateName = '祁连家园'
     Distinct = '宝山'
     AreaName = '上大'
     Address = '祁连山路2555弄'
     BuildYear = '2006-07'
     Developer = '上海祁连房地产开发总公司'
     PropertyCompany = '新闸物业'
     PropertyType = '公寓'
     PropertyFee  = '1.2'
     TotalSquare = '12000平方米（中型小区）'
     TotalHouse = '586户'
     FloorAreaRatio = '1.9'
     ParkingNum = '157'
     GreenRate = '42%（绿化率高）'
     EstateLink = '/community/view/8683'
else:
    bsObj = getbsobj( 'http://shanghai.anjuke.com'  + SearchUrl)

    div = bsObj.findAll('div',{'class','comm-list'})[0]

    divA = div.contents[1]
    divB = div.contents[3]


    EstateName = divA.contents[2].string
    print(EstateName)
    Distinct = divA.contents[6].contents[0].string.strip()
    AreaName = divA.contents[6].contents[2].string.strip()
    BuildYear = divB.contents[8].string
    Address = divA.contents[9].contents[0].string
    Developer = divA.contents[12].string
    PropertyCompany =divA.contents[15].string
    PropertyType =divA.contents[18].string
    PropertyFee = divA.contents[21].string
    TotalSquare = divB.contents[2].string
    TotalHouse = divB.contents[5].string
    FloorAreaRatio = divB.contents[11].string
    ParkingNum = divB.contents[17].string
    GreenRate = divB.contents[20].string
    EstateLink = SearchUrl

sql = SqliteOpenClass()

estateid = uuid.uuid1()
sql.insertestate(estateid,EstateName,Distinct,AreaName,TotalSquare,TotalHouse,BuildYear,FloorAreaRatio,ParkingNum,GreenRate,Address,Developer,PropertyType,PropertyFee,PropertyCompany,1)
sql.insertestatelink(AreaName,EstateName,EstateLink)
sql.insertEstateAlias(estateid,EstateName,AliasB,AliasC,AliasD)
sql.insertTrafficBasicInfo("上海市" + Distinct + "区" + Address,estateid,EstateName)
getlocation("上海市" + Distinct + "区" + Address)

print('成功！')




# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import time
import threading

class GRFY:
    def __init__(self, threadno):
        self.THREADNO = threadno
        self.LastUrl = ''
        self.BaseUrl = 'http://sh.fangtan007.com'
        self.thread_stop = False
        self.StartUrl = "http://sh.fangtan007.com/chuzu/fangwu/w02/"

    def run(self):
        self.crawler(self.StartUrl)

    def stop(self):
        self.thread_stop = True

    def crawler(self,StartUrl):
        "http://sh.grfy.net/rent/list_2_0_0_0-0_0_0-0_0_2_0_1_.html"
        LoopMark = True
        urlbuff = ''
        while LoopMark == True:
            if urlbuff != '':
                self.LastUrl = urlbuff
            urlbuff = ''
            import time
            time.sleep(60)  #每隔60s 启动一次查询
            html = urlopen(StartUrl)
            bsObj = BeautifulSoup(html.read())
            UrlList = bsObj.findAll(id="list")[0].contents[1].contents
            for EleLi in UrlList:
                try:
                    href = EleLi.contents[1].contents[0].attrs['href']
                    time = EleLi.contents[7].text
                    minite = int(re.findall('\d+',time)[0])
                    if len(re.findall(unicode('分钟','utf8') + '?',time)):
                        if minite != 1:
                            break

                    if self.LastUrl == href:
                        break;

                    if urlbuff == '':
                        urlbuff = href

                    #说明是新的信息，需要载入进来
                    self.crawler_level2(href)
                except:
                    continue

    def crawler_level2(self,SearchUrl):
        html = urlopen(self.BaseUrl + SearchUrl)
        bsObj = BeautifulSoup(html.read())
        try:
            content = bsObj.findAll("div",{"class","cr_left"})[0]
            price = content.contents[1].contents[3].contents[0].string
            rooms = content.contents[3].contents[3].contents[0].string.split('-')[0]
            square = content.contents[3].contents[3].contents[0].string.split('-')[1]
            EstateName = content.contents[5].contents[3].string
            District = content.contents[7].contents[3].string.split('-')[1]
            Area = content.contents[7].contents[3].string.split('-')[2]
            Address = content.contents[7].contents[3].string.split('-')[3]
            Orientation = content.contents[9].contents[3].string.split('-')[1]
            type = content.contents[9].contents[3].string.split('-')[2]
            floor = re.findall("\d+",content.contents[11].contents[3].string.split('/')[0])[0]
            floorAll = re.findall("\d+",content.contents[11].contents[3].string.split('/')[1])[0]
            LandLadyName = content.contents[13].contents[3].string
            LandLadyPhone = content.contents[15].contents[3].string
            desc = bsObj.findAll("div",{"class","des"})
            describe = desc[0].contents[0].string + desc[0].contents[2]

            Sqlite = SqliteOpenClass()
            standardName = Sqlite.getestatename(EstateName,Address)

            countr =  re.findall("\d+",rooms)[0]
            counth =  re.findall("\d+",rooms)[1]
            countt =  re.findall("\d+",rooms)[2]

            #判断房源类型类型，根据描述中关键词判断
            sourceType = checkSourceType(describe)

            if standardName == '':
                return
            else :
                id = uuid.uuid1()
                Sqlite.inserthouse(id,EstateName,floorAll,floor,'','unknown','unknown',type,"整租","普通装修",
                                   sourceType,LandLadyName,LandLadyPhone,price,"面议",countt,counth,countr,square,
                                   Orientation,'',self.BaseUrl + SearchUrl,describe,District,Area)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            pass



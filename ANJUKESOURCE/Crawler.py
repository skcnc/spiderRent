# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re

class ANJUKE:
    def __init__(self, threadno):
        self.THREADNO = threadno
        self.LastUrl = ''

    def crawler(self,StartUrl):
        "http://sh.zu.anjuke.com/fangyuan/l2-px3/?kw=%E4%B8%AA%E4%BA%BA%E6%88%BF%E6%BA%90&cw=%E4%B8%AA%E4%BA%BA%E6%88%BF%E6%BA%90"
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
            UrlList = bsObj.findAll("div",{'class','zu-itemmod'})
            count = 0
            for EleLi in UrlList:
                try:
                    href = EleLi.contents[3].contents[1].contents[0].attrs['href']
                    count += 1
                    if self.LastUrl == href:
                        break

                    if count >= 20:
                        break

                    if urlbuff == '':
                        urlbuff = href
                    #说明是新的信息，需要载入进来
                    self.crawler_level2(href)
                except:
                    continue

    def crawler_level2(self,SearchUrl):
        html = urlopen(SearchUrl)
        bsObj = BeautifulSoup(html.read())
        try:
            price = bsObj.findAll("span",{"class","f26"})[0].string
            rooms = bsObj.findAll("dl",{"class","p_phrase"})[2].contents[3].string
            square = bsObj.findAll("dl",{"class","p_phrase"})[7].contents[3].string
            EstateName = bsObj.findAll("dl",{"class","p_phrase"})[11].contents[3].contents[1].string
            Distinct = bsObj.findAll("dl",{"class","p_phrase"})[5].contents[3].contents[0].string
            Area = bsObj.findAll("dl",{"class","p_phrase"})[5].contents[3].contents[2].string
            Address = bsObj.findAll("dl",{"class","p_phrase"})[13].contents[3].contents[0]
            Orientation = bsObj.findAll("dl",{"class","p_phrase"})[8].contents[3].string
            type = bsObj.findAll("dl",{"class","p_phrase"})[10].contents[3].string
            floor =bsObj.findAll("dl",{"class","p_phrase"})[9].contents[3].string.split('/')[0]
            floorAll = bsObj.findAll("dl",{"class","p_phrase"})[9].contents[3].string.split('/')[1]
            LandLadyName = bsObj.findAll(id='broker_true_name')[0].string
            LandLadyPhone = bsObj.findAll("div",{"class","broker_tel"})[0].contents[1]
            appliance = ''
            try:
                content = bsObj.findAll("div",{"class","pro_links"})[0].contents[1]
                for ele in content:
                    if ele.name == 'span':
                        appliance += ele.text + '/'
            except:
                appliance = '未知'

            describe = bsObj.findAll("div",{"class","pro_con"})[0].text

            Sqlite = SqliteOpenClass()
            standardName = Sqlite.getestatename(EstateName,Address)

            countr =  re.findall("\d+",rooms)[0]
            counth =  re.findall("\d+",rooms)[1]
            countt =  re.findall("\d+",rooms)[2]

            #判断房源类型类型，根据描述中关键词判断
            sourceType = "个人房源"

            if standardName == '':
                return
            else :
                id = uuid.uuid1()
                Sqlite.inserthouse(id,EstateName,floorAll,floor,'','unknown','unknown',type,"整租","普通装修",
                                   sourceType,LandLadyName,LandLadyPhone,price,"面议",countt,counth,countr,square,
                                   Orientation,'', SearchUrl,describe,Distinct,Area)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            pass



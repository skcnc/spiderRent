# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import threading
from Utils.Opener import *

class WUBATONGCHENG(threading.Thread):
    "58同城"
    def __init__(self, threadno):
        self.THREADNO = threadno
        self.LastUrl = ''
        self.BaseUrl = 'http://sh.fangtan007.com'
        self.thread_stop = False

    def run(self,StartUrl):
        self.crawler(StartUrl)

    def stop(self):
        self.thread_stop = True

    def crawler(self,StartUrl):
        "http://sh.fangtan007.com/fangwu/w01/"
        urlbuff = ''
        while self.thread_stop == False:
            if urlbuff != '':
                self.LastUrl = urlbuff
            urlbuff = ''
            import time
            time.sleep(3)  #每隔30s 启动一次查询
            bsObj = getbsobj(StartUrl)
            UrlList = bsObj.findAll("div",{'class','sub-left-list'})[0].contents[1]
            count = 0
            for EleLi in UrlList:
                try:
                    href = EleLi.findAll('div',{"class","houseinfo-name"})[0].contents[0].contents[0].attrs['href']
                    count += 1
                    if self.LastUrl == href:
                        break

                    if count >= 20:
                        break

                    if urlbuff == '':
                        urlbuff = href
                    #说明是新的信息，需要载入进来
                    self.crawler_level2(self.BaseUrl + href)
                except:
                    continue

    def crawler_level2(self,SearchUrl):
        bsObj = getbsobj(SearchUrl)
        try:
            LandLadyPhone = bsObj.findAll(id='tel')[0].string
            Urls = re.findall('(http:\/\/[\w]+[\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])',bsObj.findAll("script")[12].text)
            SourceUrl = ''
            for url in Urls:
                if "58.com" in url and 'html' in url:
                    SourceUrl = url
                    break
            if SourceUrl == '':
                return
            sourceHtml = urlopen(SourceUrl)
            sourcebsObj = BeautifulSoup(sourceHtml.read())
            price = sourcebsObj.findAll("em",{"class","house-price"})[0].string
            rooms = sourcebsObj.findAll("div",{"class","house-type"})[0].string.split('-')[0]
            square = sourcebsObj.findAll("div",{"class","house-type"})[0].string.split('-')[0]
            EstateName = sourcebsObj.findAll("div",{"class","xiaoqu"})[0].contents[1].string
            Distinct = sourcebsObj.findAll("div",{"class","xiaoqu"})[0].contents[0].string
            Area =sourcebsObj.findAll("div",{"class","xiaoqu"})[0].contents[1].string
            Sqlite = SqliteOpenClass()
            Address = ''
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
                                   Orientation,'', SearchUrl)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            pass



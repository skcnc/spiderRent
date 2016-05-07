# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import threading
from Utils.Opener import *

class GANJI(threading.Thread):
    "赶集网"
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
                if "ganji.com" in url and 'htm' in url:
                    SourceUrl = url
                    break
            if SourceUrl == '':
                return
            sourceHtml = urlopen(SourceUrl)
            sourcebsObj = BeautifulSoup(sourceHtml.read())
            price = sourcebsObj.findAll("b",{"class","basic-info-price"})[0].contents[0].string

            square = ''
            floorAll = ''
            floor = ''
            decoration = ''
            Orientation = ''
            type = ''
            LandLadyName = ''
            Address = ''
            appliance = ''
            rentType=''
            for ele in sourcebsObj.findAll("ul",{"class","basic-info-ul"})[0].contents:
                try:
                    prop = re.sub('[\t\r\n ]','',ele.text)
                except:
                    continue;
                if "户型" in prop:
                    try:
                        roomprops1 = prop.split('-')
                        for state in roomprops1:
                            if "室" in state and '卫' in state:
                                rooms = state
                            elif 'm²' in state:
                                square = state
                            else:
                                rentType = state
                    except:
                        pass
                elif "概况" in prop:
                    for state in prop.split('：')[1].split('-'):
                        if '装修' in state or "毛坯" in state:
                            decoration = state
                        elif '东' in state or '西' in state or '南' in state or '北' in state:
                            Orientation = state
                        else:
                            type = state
                elif "小区" in prop:
                    position = re.sub('[\t\n\r ]','',ele.contents[3].text).split('-')
                    Distinct = position[0]
                    if len(position) == 3:
                        Area = position[1]
                    else:
                        Area = ''

                    EstateName = position[len(position)-1]
                    if '(' in EstateName:
                        EstateName = EstateName.split('(')[0]
                    elif '（' in EstateName:
                        EstateName = EstateName.split('（')[0]
                elif "楼层" in prop:
                    floor = re.findall('(\d+)',prop)[0]
                    floorAll = re.findall('(\d+)',prop)[1]
                elif "地址" in prop:
                    Address = re.sub('[\t\n\r ]','',ele.contents[3].text)
                elif "配置" in prop:
                    appliance = re.sub('[\t\n\r ]','',ele.contents[3].text)
                elif "联系" in prop:
                    try:
                        LandLadyName = re.findall('([\W]+)\(',re.sub('[\r\n\t ]','',ele.contents[3].text))[0]
                    except:
                        pass

            #图片列表
            pics = ''
            for ele in sourcebsObj.findAll("li",{"class","house-images-wrap"}):
                pics += ele.contents[0].attrs['lazy_src'] + "|"

            Sqlite = SqliteOpenClass()

            describe = re.sub('[\r\n\t ]','',sourcebsObj.findAll("div",{"class","description-content"})[0].text)

            standardName = Sqlite.getestatename(EstateName,Address)

            countr =  re.findall(unicode("(\d+)室"),rooms)[0]
            counth =  re.findall(unicode("(\d+)厅"),rooms)[0]
            countt =  re.findall(unicode("(\d+)卫"),rooms)[0]

            #判断房源类型类型，根据描述中关键词判断
            sourceType = "个人房源"
            if standardName == '':
                return
            else :
                id = uuid.uuid1()
                Sqlite.insertpiclinks(id,pics)
                Sqlite.inserthouse(id,EstateName,floorAll,floor,'','unknown','unknown',type,rentType,decoration,
                                   sourceType,LandLadyName,LandLadyPhone,price,"面议",countt,counth,countr,square,
                                   Orientation,appliance, SearchUrl)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            pass


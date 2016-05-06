# -*- coding: utf-8 -*-
import threading
import time
from urllib import urlopen
from sqliteOper.Operations import *
from bs4 import BeautifulSoup


class anjukeOper:
    def __init__(self):
        self.matrixName = {}
        self.matrixDic = {}
        self.curse = 0
        self.UrlList = []
        #self.db = SqliteOpenClass()
        self.CityId = "1"

    def GetAreaInfo(self,urlBase):
        "获取区县和地域列表，并返回包含区县名称的二维数据和地域链接地址"
        html = urlopen(urlBase)
        bsObj = BeautifulSoup(html.read())
        elelist = bsObj.findAll("span",{"class","elems-l"})[0]
        for ele in elelist.contents:
            try:
                href = ele.attrs['href']
                name = ele.string
                if href == "http://shanghai.anjuke.com/community/":
                    continue

                DisId = uuid.uuid1()
                #self.db.insertdistinct(DisId,name,self.CityId)
                self.GetSubAreaInfo(href,name,DisId)
            except:
                pass
        l1Thread = XQList()
        l2Thread = XQList()
        l3Thread = XQList()
        l4Thread = XQList()
        l1Thread.url = ''
        l2Thread.url = ''
        l3Thread.url = ''
        l4Thread.url = ''
        l1Thread.start()
        l2Thread.start()
        l3Thread.start()
        l4Thread.start()
        print("队列长度：" + str(len(self.UrlList)))
        for link in self.UrlList:
            time.sleep(1)
            wait = False
            while wait == False:
                if bool(l1Thread.completed) == True:
                    l1Thread.url = link
                    break
                if bool(l2Thread.completed) == True:
                    l2Thread.url = link
                    break
                if bool(l3Thread.completed) == True:
                    l3Thread.url = link
                    break
                if bool(l4Thread.completed) == True:
                    l4Thread.url = link
                    break
            continue
        time.sleep(20)
        l1Thread.stop_mark = True
        l2Thread.stop_mark = True
        l3Thread.stop_mark = True
        l4Thread.stop_mark = True
        print("全部搜索完成！")

    def GetSubAreaInfo(self,Url,level1name,disId):
        "获取二级地域信息"
        html = urlopen(Url)
        bsObj = BeautifulSoup(html.read())
        elelist = bsObj.findAll("div",{"class","sub-items"})
        for sibling in elelist[0].children:
            try:
                if Url == sibling.attrs['href']:
                    continue
                self.matrixDic[sibling.attrs['title']] = sibling.attrs['href']
                self.matrixName[sibling.attrs['title']] = level1name
                self.UrlList.append(sibling.attrs['href'])
                id = uuid.uuid1()
                name = sibling.attrs['title']
                #self.db.insertarea(id,name,disId,self.CityId)
            except:
                pass
        print("GetSubAreaInfo")

class XQList(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.XQList = []
        self.completed = True
        self.threadCount = 20

    def run(self):
        self.stop_mark = False
        while self.stop_mark == False:
            if self.url == '':
                self.completed = True
            if self.url != '':
                self.completed = False
                self.XQList = []
                self.GetXQList(self.url)
                self.url = ''
            time.sleep(1)

    def GetXQList(self,baseUrl):
        "获取指定URL下的房产列表"
        baseUrl += "p"
        page = 1
        Url = baseUrl + str(page) + "/"
        html = urlopen(Url)
        bsObj = BeautifulSoup(html.read())
        try:
            areaName = bsObj.findAll("span",{"class","tit"})[0].findAll("em")[0].string
            XQCOUNT = bsObj.findAll("span",{"class","tit"})[0].findAll("em")[1].string
        except:
            print("获取失败：" + Url)
            return
        count = 0
        var = 1
        while var == 1:
            if str(count) == XQCOUNT:
                print("URL " + baseUrl + "共计" + str(count))
                break
            page += 1
            Url = baseUrl + str(page) + "/"
            elelist = bsObj.findAll("",{"class","li-itemmod"})
            for ele in elelist:
                try:
                    xqlink = ele.contents[1].attrs['href']
                    xqname = ele.contents[1].attrs['title']
                    count += 1
                    stringli = xqlink
                    self.XQList.append(stringli)
                except:
                    continue;
            html = urlopen(Url)
            bsObj = BeautifulSoup(html.read())


        threads = []
        i = 0
        while i < self.threadCount:
            t = XQinfo(i)
            t.url = ''
            t.start()
            threads.append(t)
            i += 1

        var = False
        print("总计：" + str(len(self.XQList)))
        for xqstr in self.XQList:
            time.sleep(0.1)
            while var == False:
                sendmark = False
                for work in threads:
                    if work.completed == True:
                        work.url = xqstr
                        sendmark = True
                        break
                    else:
                        continue
                if sendmark == True:
                    break
        while var == False:
            count = 0
            for work in threads:
                if work.completed == True:
                    count += 1
            if count == self.threadCount:
                break
        print("任务已经分发完成！")
        return

class XQinfo(threading.Thread):
    def __init__(self,threadno):
        threading.Thread.__init__(self)
        self.XQList = {}
        self.completed = True
        self.db = SqliteOpenClass()
        self.CityId = "1"
        self.url = ''
        self.baseUrl = 'http://shanghai.anjuke.com'
        self.threadno = threadno

    def stop(self):
        self.stop_mark = True

    def run(self):
        self.stop_mark = False
        while self.stop_mark == False:
            if self.url == '':
                self.completed = True
            else:
                self.completed = False
                self.GetXQInfo(self.baseUrl + self.url)
                print("线程： " + str(self.threadno) + "  URL:  " + self.url)
                time.sleep(1)
                self.url = ''
            continue

    def GetXQInfo(self,URL):
        try:
            html = urlopen(URL)
            bsObj = BeautifulSoup(html.read())
            profileA  = bsObj.findAll("dl",{"class","comm-l-detail"})[0]
            profileB = bsObj.findAll("dl",{"class","comm-r-detail"})[0]
            EstateName = profileA.contents[2].string
            distinct = profileA.contents[6].contents[0].attrs["title"]
            area = profileA.contents[6].contents[2].attrs["title"]
            TotalSquare = profileB.contents[2].string
            TotalHouse = profileB.contents[5].string
            BuildYear = profileB.contents[8].string

            FloorAreaRatio = profileB.contents[11].string
            ParkingNum = profileB.contents[17].string
            GreenRate = profileB.contents[20].string
            Address = profileA.contents[9].contents[0].string
            Developer = profileA.contents[12].string
            PropertyCompany = profileA.contents[15].string
            PropertyType = profileA.contents[18].string
            PropertyFee = profileA.contents[21].string
            id = uuid.uuid1()
            self.db.insertestate(id,EstateName,distinct,area,TotalSquare,TotalHouse,BuildYear,FloorAreaRatio,ParkingNum, \
            GreenRate,Address,Developer,PropertyType,PropertyFee,PropertyCompany,self.CityId)
            self.db.updatestatelink(self.url)
        except Exception as e:
            print(e)
            print("失败链接 ：" + URL)
            return

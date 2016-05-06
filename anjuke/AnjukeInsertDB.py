# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from bs4 import BeautifulSoup

level1link = {}
def GetAreaInfo(urlBase):
    "获取区县和地域列表，并返回包含区县名称的二维数据和地域链接地址"
    html = urlopen(urlBase)
    bsObj = BeautifulSoup(html.read())
    elelist = bsObj.findAll("span",{"class","elems-l"})[0]
    db = SqliteOpenClass()
    for ele in elelist.contents:
        try:
            href = ele.attrs['href']
            name = ele.string
            if href == "http://shanghai.anjuke.com/community/":
                continue
            level1link[name] = href
        except:
            pass
    loadSubArea()

def loadSubArea():
    db = SqliteOpenClass()
    arr = db.getdistinct()
    for dis in arr:
        disId = dis[1]
        link = level1link[dis[0]]
        html = urlopen(link)
        bsObj = BeautifulSoup(html.read())
        elelist = bsObj.findAll("div",{"class","sub-items"})
        for sibling in elelist[0].children:
            try:
                if link == sibling.attrs['href']:
                    continue
                sublink= sibling.attrs['href']
                name = sibling.attrs['title']
                id = uuid.uuid1()
                db.insertarea(id,name,disId,"1",sublink)
            except:
                pass
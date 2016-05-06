# -*- coding: utf-8 -*-
from anjuke.HtmlOper import *
from anjuke.AnjukeInsertDB import *
from urllib import urlopen
from bs4 import BeautifulSoup
import threading
import time

#anjuke = anjukeOper()
#anjuke.GetAreaInfo("http://shanghai.anjuke.com/community/")
#GetAreaInfo("http://shanghai.anjuke.com/community/")

ts = []
var = 0

while var < 10:
    ts.append(XQinfo(var))
    ts[var].url = ''
    ts[var].tno = var
    ts[var].start()
    var += 1

db = SqliteOpenClass()
arr = db.getestatelink()

time.sleep(1)

if arr is None:
    print(" arr is none !")

while len(arr) != 0:
    for row in arr:
        try:
            name = row[0]
            link = row[1]
            mark = row[2]
            if mark == "Y":
                continue
            for work in ts:
                time.sleep(0.1)
                if work.completed == True:
                    work.url = link
                    print(work.tno + "  " + name + "  " + link)
                    time.sleep(0.5)
                    break
        except:
            print(row[0] + "|" + row[1] + "|" + row[2])
    arr = db.getestatelink()

for work in ts:
    work.stop()
print("搜索结束")

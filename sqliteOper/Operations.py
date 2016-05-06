#-*- coding: UTF-8 -*-
import sqlite3
import uuid
import time
import threading

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SqliteOpenClass:
    def __init__(self):
        self.lock = threading.RLock()
        self.dbpath = 'F:\项目文档\SpiderCrawler\HouseDB\HouseInfo'

    def get_conn(self):
        conn = sqlite3.connect( self.dbpath )
        return conn

    def conn_close(self,conn=None):
        conn.close()

    def save(self,sql, conn=None):
        conn.execute(sql)

    def insertdistinct(self,disId,distinctName,CityId):
        if distinctName.strip() == '':
            pass
        name = unicode(distinctName)
        sql = "INSERT INTO Dics VALUES ('{0}','{1}','{2}')".format(disId,name,CityId)
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def getestatelink(self):
        sql = "SELECT ESTATENAME, ESTATELINK, MARK FROM ESTATELINK where mark = 'N'"
        connection = self.get_conn()
        cur = connection.execute(sql)
        arr = []
        time.sleep(0.01)
        for row in cur:
            try:
                arr.append(row)
            except:
                print(row)
        self.conn_close(connection)
        return arr

    def getestatename(self,name,address):
        "小区名字重复性判断"
        name = name.strip()
        sql = "SELECT AliasA FROM EstateAlias WHERE AliasA like '%{0}%' OR AliasB like '%{1}%' OR AliasC like '%{2}%' OR AliasD like '%{3}%'".format(name,name,name,name)
        connection = self.get_conn()
        cur = connection.execute(sql)
        time.sleep(0.01)
        if cur.arraysize == 0:
            sqlInsert = "INSERT INTO UnKnownEstateName VALUES ('{0}','{1}')".format(name,address)
            connection.execute(sqlInsert)
            self.conn_close(connection)
            return ''
        else :
            self.conn_close(connection)
            return name

    def updatestatelink(self,link):
        sql = "UPDATE ESTATELINK SET MARK = 'Y' WHERE ESTATELINK LIKE '%{0}%'".format(link.strip('\n'))
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def insertestatelink(self,area, name,link):
        sql = "INSERT INTO ESTATELINK VALUES ('{0}','{1}','{2}')".format(area ,name,link)
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def insertarea(self,AreaId,AreaName,DistinctId,CityId,Sublink):
        sql = "INSERT INTO AREA (AreaID, AreaName,DistinctID,CityID,xqlistLink)" \
            "VALUES ('{0}','{1}','{2}','{3}','{4}')".format(AreaId,AreaName,DistinctId,CityId,Sublink)
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def insertestate(self,estateId, EstateName,distinct,area,TotalSquare,TotalHouse,BuildYear,FloorAreaRatio,ParkingNum,GreenRate,\
                     Address,Developer,PropertyType,PropertyFee,PropertyCompany,CityId):
        sql = " INSERT INTO Estate (EstateID,EstateName,DistinctID,CityID,BuildYear,Address,Developer," \
                "PropertyCompany,PropertyType,PropertyFee,TotalSquare,TotalHouse,FloorAreaRatio,ParkingNum,GreenRate)" \
                " values ('{0}', '{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}')".format(estateId,\
                EstateName,distinct,CityId,BuildYear,Address,Developer,PropertyCompany,PropertyType,PropertyFee,TotalSquare,\
                TotalHouse,FloorAreaRatio,ParkingNum,GreenRate)
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()

    def inserthouse(self,houseId,EstateName,FloorAll,Floor,FloorLevel,RoomNum,BuildingNo,Type,RentType,
                    Decoration,HouseSourceType,LandladyName,LandLadyPhone,RentPrice,PriceType,CountT,CountH,CountR,
                    Square,Orientation,Appliance,link):
        ISOTIMEFORMAT="%Y-%m-%d %X"
        curtime = time.strftime(ISOTIMEFORMAT, time.localtime())

        sql_insert_house = "INSERT INTO House VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(
            houseId,EstateName,curtime,str(FloorAll),str(Floor), '',RoomNum,BuildingNo,Type)

        sql_insert_houseinfo = "INSERT INTO HouseInfo VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')".format(
            houseId,RentType,Decoration,HouseSourceType,LandladyName,LandLadyPhone,RentPrice,RentType,str(CountT),str(CountH),str(CountR),str(Square),
            Orientation,Appliance,curtime,link)

        conn = sqlite3.connect(self.dbpath)
        conn.execute(sql_insert_house)
        conn.execute(sql_insert_houseinfo)
        conn.commit()
        conn.close()

    def insertUnknowndesc(self,describe):
        sql = "INSERT INTO UnKnownDescWord VALUES ('{0}')".format(describe)
        conn = sqlite3.connect(self.dbpath)
        conn.execute(sql)
        conn.commit()
        conn.close()








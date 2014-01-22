#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from PyQt5 import QtCore
import peewee as pw

import db.models
from utils import six
from datetime import datetime
from gui.qobject import QObjectListModel, ObjectWrapper, postGui
from gui import signals as guiSignals
from core.signals import query_trains_completed, query_tickets_completed
from core.poster import SEAT_TYPE, JSON_SEAT, poster
from db import signals as dbSignals
from db.models import common_db, user_db, Station, Passenger, UserHistory

def peeweeWrapper(instance):
    params = instance.__dict__['_data']
    ret = {}
    for k, v in six.iteritems(params):
        ret[stringTitle(k)] = v
    return ObjectWrapper(ret)

def stringTitle(name):
    names = name.split("_")
    lasts = "".join(map(lambda name: name.title(), names[1:]))
    return "%s%s" % (names[0], lasts)

class BaseModel(QObjectListModel):
        
    instanceRole = QtCore.Qt.UserRole + 1
    _roles = { instanceRole : "instance" }

    def data(self, index, role):
        if not index.isValid() or index.row() > self.size():
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        if role == self.instanceRole:
            return item
        return QtCore.QVariant()        
    
    @QtCore.pyqtSlot("QVariant")        
    def addObj(self, obj):
        self.append(obj)
        
    @QtCore.pyqtSlot("QVariant")    
    def removeObj(self, obj):
        self.remove(obj)
    

class TrainModel(BaseModel):
    
    SeatSorted = "商务座 特等座 一等座 二等座 高级软卧 软卧 硬卧 软座 硬座 无座 其他".split()
    
    def __init__(self, parent=None, connectSignals=True):
        super(TrainModel, self).__init__(parent)
        if connectSignals:
            query_trains_completed.connect(self.onQueryTrainsCompleted, sender=self)
            query_tickets_completed.connect(self.onQueryTicketsCompleted, sender=self)
            
        now = datetime.now()
        self._today = QtCore.QDate(now.year, now.month, now.day)        
        self._dateObj = QtCore.QDate(now.year, now.month, now.day)        
        
    @classmethod    
    def parseQuery(cls, queryItem):    
        result = {}
        seats = []
        for k, v in six.iteritems(queryItem):
            nk = stringTitle(k)
            if k in JSON_SEAT and v != "--":
                try: numValue = int(v)
                except: numValue = 0    
                seat = dict(name=JSON_SEAT[k], num=numValue)                
                seats.append(ObjectWrapper(seat))
            else:    
                result[nk] = v
        seats = sorted(seats, key=lambda item: cls.SeatSorted.index(item.name))        
        result['seats'] = seats
        result['fromStationType'] = cls.getFromStationType(result)
        result['toStationType'] = cls.getToStationType(result)
        result['lishi'] = cls.parseLishiValue(result['lishiValue'])
        result['buttonTextInfo'] = result['note'].replace("<br/>", '    ')
        result['canBuy'] = "br" not in result['note']
        return result
    
    @classmethod
    def parseTicketQuery(cls, queryItem):
        result = {}
        seats = []
        queryLeftNewDTO = queryItem.pop("queryLeftNewDTO", {})
        result['buttonTextInfo'] = queryItem.pop("buttonTextInfo", "")
        result['secretStr'] = queryItem.pop("secretStr", "")
        for k, v in six.iteritems(queryLeftNewDTO):
            nk = stringTitle(k)
            if k in JSON_SEAT and v != "--":
                if v == "无": v = 0
                seat = dict(name=JSON_SEAT[k], num=v)                
                seats.append(ObjectWrapper(seat))
            else:    
                result[nk] = v
        seats = sorted(seats, key=lambda item: cls.SeatSorted.index(item.name))        
        result['seats'] = seats
        result['fromStationType'] = cls.getFromStationType(result)
        result['toStationType'] = cls.getToStationType(result)
        result['lishi'] = cls.parseLishiValue(result['lishiValue'])
        result['canBuy'] = "br" not in result['buttonTextInfo']
        result['buttonTextInfo'] = result['buttonTextInfo'].replace("<br/>", '    ')
        return result
    
    @classmethod
    def getFromStationType(cls, result):
        startName = result["startStationTelecode"]
        fromName = result["fromStationTelecode"]
        if startName == fromName:
            return "始"
        return "过"
    
    @classmethod
    def getToStationType(cls, result):
        endName = result["endStationTelecode"]
        toName = result["toStationTelecode"]
        if endName == toName:
            return "终"
        return "过"
    
    @classmethod
    def parseLishiValue(self, value):
        value = int(value)
        x = value / 60
        mod = value % 60
        if x < 1:
            return "{0:0>2}分钟".format(value)
        # if mod == 0:
        #     return "{0:0>2}小时".format(x)
        return "{0:0>2}小时{1:0>2}分钟".format(x, mod)
    
    def handleItem(self, item):
        return ObjectWrapper(item)
    
    @postGui()
    def onQueryTrainsCompleted(self, data, *args, **kwargs):
        self.clear()
        if data is None:
            return 
        for item in data:
            self.append(self.handleItem(self.parseQuery(item)))
            
    @postGui()        
    def onQueryTicketsCompleted(self, data, *args, **kwargs):
        self.clear()
        if data is None:
            return 
        for item in data:
            self.append(self.handleItem(self.parseTicketQuery(item)))
            
    @QtCore.pyqtSlot(str, str, str)    
    def queryTrains(self, fromStation, toStation, date):
        self._fromStation = fromStation
        self._toStation = toStation
        self._date = date
        self._dateObj = QtCore.QDate(*list(map(int, date.split("-"))))
        poster.query_tickets(fromStation, toStation, date, sender=self)
        
    @QtCore.pyqtSlot(str)    
    def removeByTrainCode(self, trainCode):
        obj = None
        for item in self:
            if item.stationTrainCode == trainCode:
                obj = item
                break
        self.remove(obj)    
        
    def queryByDay(self, date):    
        guiSignals.calendar_date_changed.send(sender=self, date=self._dateObj)
        try:
            poster.query_tickets(self._fromStation, self._toStation, date, sender=self)
        except:    
            pass
        
    @QtCore.pyqtSlot()    
    def previousDay(self):    
        if self._dateObj <= self._today:
            return        
        self._dateObj = self._dateObj.addDays(-1)
        date = self._dateObj.toString("yyyy-MM-dd")
        self.queryByDay(date)
    
    @QtCore.pyqtSlot()
    def nextDay(self):
        self._dateObj = self._dateObj.addDays(1)
        date = self._dateObj.toString("yyyy-MM-dd")
        self.queryByDay(date)
        
    @QtCore.pyqtSlot("QVariant")    
    def queryByDate(self, date):
        self._dateObj = date
        self.queryByDay(self._dateObj.toString("yyyy-MM-dd"))
    
class PopupTrainModel(TrainModel):        
    
    def __init__(self, selectMoel, parent=None, connectSignals=True):
        super(PopupTrainModel, self).__init__(parent, connectSignals)
        
        self._selectModel = selectMoel
        
    def handleItem(self, item):    
        trainCode = item['stationTrainCode']
        item["checked"] = False
        for obj in self._selectModel:
            if obj.stationTrainCode == trainCode:
                item['checked'] = True
                break
        return super(PopupTrainModel, self).handleItem(item)
                
class StationModel(BaseModel):        
    
    @QtCore.pyqtSlot(str)
    def complete(self, text):
        self.clear()
        if text == "":
            return 
        stations = Station.select().where(
            (pw.fn.Lower(pw.fn.Substr(Station.jian, 1, len(text))) == text) |
            (pw.fn.Lower(pw.fn.Substr(Station.quan, 1, len(text))) == text) |
            (pw.fn.Lower(pw.fn.Substr(Station.name, 1, len(text))) == text) 
        )
        for s in stations:
            self.append(peeweeWrapper(s))
            
    @QtCore.pyqtSlot(int, result=str)        
    def getTelecode(self, index):
        try:
            obj = self._data[index]
        except IndexError:    
            return ""
        else:
            return obj.telecode 
        
class PassengerModel(BaseModel):
    
    def __init__(self, parent=None, connectSignals=True):
        super(PassengerModel, self).__init__(parent)
        if connectSignals:
            dbSignals.db_init_finished.connect(self.onDBInitFinished, sender=user_db)
            dbSignals.post_save.connect(self.onPostSave, sender=Passenger)
        
    @postGui()    
    def onDBInitFinished(self, created, *args, **kwargs):
        if not created:
            self.addAllPassengers()
            
    def addAllPassengers(self):        
        query = Passenger.select()
        for item in query:
            self.append(peeweeWrapper(item))
            
    @postGui()        
    def onPostSave(self, instance, *args, **kwargs):
        self.append(peeweeWrapper(instance))

class UserHistoryModel(BaseModel):        
    
    def __init__(self, parent=None):
        super(UserHistoryModel, self).__init__(parent)
        if db.models.COMMON_DB_INITED:
            self.addAllUser()
        else:    
            dbSignals.db_init_finished.connect(self.onDBInitFinished, sender=common_db)
        
    def addAllUser(self):    
        query = UserHistory.select()
        for item in query:
            self.append(peeweeWrapper(item))
        
    @postGui()    
    def onDBInitFinished(self, created, *args, **kwargs):    
        if not created:
            self.addAllUser()

    @QtCore.pyqtSlot(result="QVariant")            
    def getLastUser(self):
        if self.size() > 0:
            return self._data[-1]
        return None
    
class SeatModel(BaseModel):
    
    def __init__(self, parent=None, initSeats=True):
        super(SeatModel, self).__init__(parent)
        
        if initSeats:
            self.initSeats()

    def initSeats(self):    
        for k, v in six.iteritems(SEAT_TYPE):
            seat = dict(seatName=k, seatType=v)
            self.append(ObjectWrapper(seat))

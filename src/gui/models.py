#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from PyQt5 import QtCore

from models import six
import peewee as pw
from gui.qobject import QObjectListModel, ObjectWrapper, postGui
from core.signals import query_trains_completed, query_tickets_completed
from core.poster import SEAT_TYPE
from db.models import user_db, Station, Passenger, UserHistory
from db import signals as dbSignals

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
    

class TrainModel(BaseModel):
    
    SeatType = {
        "gr_num" : "高级软卧",
        "qt_num" : "其他",
        "rw_num" : "软卧",
        "rz_num" : "软座",
        "tz_num" : "特等座",
        "wz_num" : "无座",
        "yw_num" : "硬卧",
        "yz_num" : "硬座",
        "ze_num" : "二等座",
        "zy_num" : "一等座",
        "swz_num" : "商务座",
    }
    
    SeatSorted = "商务座 特等座 一等座 二等座 高级软卧 软卧 硬卧 软座 硬座 无座 其他".split()
    
    def __init__(self, parent=None):
        super(TrainModel, self).__init__(parent)
        query_trains_completed.connect(self.onQueryTrainsCompleted)
        query_tickets_completed.connect(self.onQueryTicketsCompleted)

        
    @classmethod    
    def parseQuery(cls, queryItem):    
        result = {}
        seats = []
        for k, v in six.iteritems(queryItem):
            nk = stringTitle(k)
            if k in cls.SeatType and v != "--":
                try: numValue = int(v)
                except: numValue = 0    
                seat = dict(name=cls.SeatType[k], num=numValue)                
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
        return ObjectWrapper(result)
    
    @classmethod
    def parseTicketQuery(cls, queryItem):
        result = {}
        seats = []
        queryLeftNewDTO = queryItem.pop("queryLeftNewDTO", {})
        result['buttonTextInfo'] = queryItem.pop("buttonTextInfo", "")
        result['secretStr'] = queryItem.pop("secretStr", "")
        for k, v in six.iteritems(queryLeftNewDTO):
            nk = stringTitle(k)
            if k in cls.SeatType and v != "--":
                if v == "无": v = 0
                seat = dict(name=cls.SeatType[k], num=v)                
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
        return ObjectWrapper(result)
    
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
    
    @postGui()
    def onQueryTrainsCompleted(self, data, *args, **kwargs):
        self.clear()
        for item in data:
            self.append(self.parseQuery(item))
            
    @postGui()        
    def onQueryTicketsCompleted(self, data, *args, **kwargs):
        self.clear()
        for item in data:
            self.append(self.parseTicketQuery(item))
        
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
    
    def __init__(self, parent=None):
        super(PassengerModel, self).__init__(parent)
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

        
class SelectPassengerModel(BaseModel):        
    
    
    @QtCore.pyqtSlot("QVariant")
    def addPassenger(self, obj):
        self.append(obj)
        
    @QtCore.pyqtSlot("QVariant")    
    def removePassenger(self, obj):
        self.remove(obj)

        
class UserHistoryModel(BaseModel):        
    
    def __init__(self, parent=None):
        super(UserHistoryModel, self).__init__(parent)
        # dbSignals.db_init_finished.connect(self.onDBInitFinished, sender=common_db)
        self.addAllUser()
        
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
        
    @QtCore.pyqtSlot("QVariant")        
    def addSeat(self, obj):        
        self.append(obj)
        
    @QtCore.pyqtSlot("QVariant")    
    def removeSeat(self, obj):
        self.remove(obj)

    def initSeats(self):    
        for k, v in six.iteritems(SEAT_TYPE):
            seat = dict(seatName=k, seatType=v)
            self.append(ObjectWrapper(seat))

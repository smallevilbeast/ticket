#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from PyQt5 import QtCore

from core import signals
from core.poster import poster, REVERSAL_JSON_SEAT, SEAT_TYPE
from gui.qobject import QPropertyObject, postGui, ObjectWrapper
from gui.models import (TrainModel, StationModel, PassengerModel,
                        UserHistoryModel, SeatModel, PopupTrainModel)
from db.models import MonitorHistory


class PosterControl(QPropertyObject()):
    __qtprops__ = {
        "passcodeUrl" : "", "queryNumber" : 0,
        "queryRemainingTime": "0.0", "grabTicketFlag" : False
    }
    
    loginSuccessed = QtCore.pyqtSignal()
    passcodeNewed = QtCore.pyqtSignal(str, str)
    passcodeChecked = QtCore.pyqtSignal(str)
    errorExcepted = QtCore.pyqtSignal(str)
    grabTicketsSuccessed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(PosterControl, self).__init__(parent)
        self._poster = poster
        
        self._queryTrainModel = TrainModel(self)
        self._selectTrainModel = TrainModel(self, connectSignals=False)        
        
        self._passengerModel = PassengerModel(self)
        self._selectPassengerModel = PassengerModel(self, False)
        self._userHistoryModel = UserHistoryModel(self)
        self._seatModel = SeatModel(self)
        self._selectSeatModel = SeatModel(self, initSeats=False)
        
        # timer
        self._queryTimer = QtCore.QTimer(self)
        self._queryTimer.setSingleShot(True)
        self._queryTimer.setInterval(3000) # 3000 milliseconds.
        self._queryTimer.timeout.connect(self.onQueryTimerTimeout)
        self._notifyTimer = QtCore.QTimer(self)
        self._notifyTimer.setInterval(100)
        self._notifyTimer.timeout.connect(self.updateRemainingTime)
        self._notifyTimer.setSingleShot(False)

        signals.passcode_newed.connect(self.onPasscodeNewed)
        signals.login_successed.connect(self.onLoginSuccessed)
        signals.passcode_checked.connect(self.onPasscodeChecked)
        signals.error_excepted.connect(self.onErrorExcepted)
        signals.query_tickets_completed.connect(self.onQueryTicketsCompleted, sender=self)
        
        # signals.query_tickets_failed
        # signals.grab_tickets_failed.connect(self.)
        signals.grab_tickets_successed.connect(self.onGrabTicketsSuccessed)
        
    def onGrabTicketsSuccessed(self, *args, **kwargs):
        self.grabTicketsSuccessed.emit()
        
    @postGui()    
    def onPasscodeNewed(self, url, module, ran_code, *args, **kwargs):    
        url = url.replace("\\", "/")
        if not url.startswith("/"):
            url = "/" + url
        self.passcodeNewed.emit(module, url)
        
    @QtCore.pyqtSlot(str)
    def newPasscode(self, module="login"):
        if module == "login": rand = "sjrand"
        elif module == "passenger": rand = "randp"
        self._poster.new_passcode(module, rand)
        
    @QtCore.pyqtSlot(str, str)
    def checkLogin(self, username, password):
        self._poster.check_login(username, password)
        
    @QtCore.pyqtSlot(str, str)    
    def checkPasscode(self, code, module="login"):
        if module == "login": rand = "sjrand"
        elif module == "passenger": rand = "randp"
        self._poster.check_passcode(code, module, rand)
        
    @QtCore.pyqtSlot(str)    
    def login(self, code):
        self._poster.login(code)

    def onLoginSuccessed(self, *args, **kwargs):    
        self.loginSuccessed.emit()

    def onErrorExcepted(self, type_, info, *args, **kwargs):    
        self.errorExcepted.emit(info)
            
    def onPasscodeChecked(self, module, *args, **kwargs):        
        self.passcodeChecked.emit(module)
    
    @QtCore.pyqtSlot(result="QVariant")
    def passengerModel(self):
        return self._passengerModel
    
    @QtCore.pyqtSlot(result="QVariant")
    def newStationModel(self):
        return StationModel(self)
    
    @QtCore.pyqtSlot(result="QVariant")
    def seatModel(self):
        return self._seatModel
    
    @QtCore.pyqtSlot(result="QVariant")
    def selectSeatModel(self):
        return self._selectSeatModel
    
    @QtCore.pyqtSlot(result="QVariant")
    def selectTrainModel(self):
        return self._selectTrainModel
    
    @QtCore.pyqtSlot(result="QVariant")
    def newTrainModel(self):
        return PopupTrainModel(self._selectTrainModel, self)
    
    @QtCore.pyqtSlot(result="QVariant")
    def queryTrainModel(self):
        return self._queryTrainModel
    
    @QtCore.pyqtSlot(result="QVariant")
    def selectPassengerModel(self):
        return self._selectPassengerModel
    
    @QtCore.pyqtSlot(result="QVariant")
    def userHistoryModel(self):
        return self._userHistoryModel
    
    @QtCore.pyqtSlot()
    def requestPassengers(self):
        self._poster.request_passengers()
        
    @QtCore.pyqtSlot("QVariant", str, "QVariant", str)    
    def grabTickets(self, train, date, passengers, seat_type):
        self._poster.grab_tickets(train, date, passengers, seat_type)
        
    @QtCore.pyqtSlot(str)
    def submitTickets(self, code):
        self._poster.submit_tickets(code)
        
    @QtCore.pyqtSlot(result="QVariant")    
    def queryTimer(self):
        return self._queryTimer
        
    @QtCore.pyqtSlot(str, str, str)    
    def addMonitor(self, fromStation, toStation, date):
        passengers = ",".join([ p.code for p in self._selectPassengerModel.getAll() ])
        seats = ",".join([ s.seatName for s in self._selectSeatModel.getAll() ])
        trains = ",".join([ t.stationTrainCode for t in self._selectTrainModel.getAll() ])
        params = dict(
            from_station=fromStation,
            to_station=toStation,
            date=date,
            passengers=passengers,
            trains=trains,
            seats=seats
        )
        MonitorHistory.create(**params)
        
    def onQueryTicketsCompleted(self, data, *args, **kwargs):    
        if data is None:
            self._queryTimer.start()
        else:
            trains = [ t.stationTrainCode for t in self._selectTrainModel.getAll() ]
            seats = [ s.seatName for s in self._selectSeatModel.getAll() ]
            for trainCode in trains:
                for item in data:
                    queryLeftNewDTO = item.get("queryLeftNewDTO")
                    if queryLeftNewDTO.get("station_train_code") == trainCode:
                        for seatName in seats:
                            seatStr = queryLeftNewDTO[REVERSAL_JSON_SEAT[seatName]]
                            if seatStr == "有" or seatStr.isdigit():
                                trainObj = ObjectWrapper(TrainModel.parseTicketQuery(item))
                                poster.grab_tickets(trainObj, self._date, self._selectPassengerModel.getAll(), SEAT_TYPE[seatName])
                                return True
                            
            self._queryTimer.start()
                                
    @QtCore.pyqtSlot(str, str, str)        
    def grabQueryTickets(self, fromStation, toStation, date):
        self._fromStation = fromStation
        self._toStation = toStation
        self._date = date
        
        self.grabTicketFlag = True
        self.queryNumber += 1
        self._notifyTimer.start()
        poster.query_tickets(fromStation, toStation, date, sender=self,  sendError=True)
        
    def onQueryTimerTimeout(self):    
        if self.grabTicketFlag:
            self.queryNumber += 1
            poster.query_tickets(self._fromStation, self._toStation, self._date, sender=self, sendError=True)
        
    def updateRemainingTime(self):    
        num = self._queryTimer.remainingTime() / 1000.0
        if num < 0:
            num = 0.0
        else:    
            num = round(num, 1)
        self.queryRemainingTime = str(num)

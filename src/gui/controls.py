#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore

from core import signals
from core.poster import poster
from gui.qobject import QPropertyObject, postGui
from gui.models import (TrainModel, StationModel, PassengerModel,
                        SelectPassengerModel, UserHistoryModel, SeatModel)


class PosterControl(QPropertyObject()):
    __qtprops__ = { "passcodeUrl" : "" }
    
    loginSuccessed = QtCore.pyqtSignal()
    passcodeNewed = QtCore.pyqtSignal()
    orderPasscodeNewed = QtCore.pyqtSignal(str)
    passcodeChecked = QtCore.pyqtSignal()
    errorExcepted = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(PosterControl, self).__init__(parent)
        self._poster = poster
        
        self._trainModel = TrainModel(self)
        self._passengerModel = PassengerModel(self)
        self._selectPassengerModel = SelectPassengerModel(self)
        self._userHistoryModel = UserHistoryModel(self)
        self._seatModel = SeatModel(self)
        self._selectSeatModel = SeatModel(self, initSeats=False)
        
        signals.passcode_newed.connect(self.onPasscodeNewed)
        signals.passcode_checked.connect(self.onPasscodeChecked)
        signals.login_successed.connect(self.onLoginSuccessed)
        signals.error_excepted.connect(self.onErrorExcepted)
        
    @postGui()    
    def onPasscodeNewed(self, url, module, ran_code, *args, **kwargs):    
        if module == "login":
            self.passcodeUrl = url
            self.passcodeNewed.emit()
        elif module == "passenger":
            self.orderPasscodeNewed.emit(url)
            
    @QtCore.pyqtSlot()
    def newPasscode(self):
        self._poster.new_passcode()
        
    @QtCore.pyqtSlot(str, str)
    def checkLogin(self, username, password):
        self._poster.check_login(username, password)
        
    @QtCore.pyqtSlot(str)    
    def checkPasscode(self, code):
        self._poster.check_passcode(code)
        
    @QtCore.pyqtSlot(str)    
    def login(self, code):
        self._poster.login(code)

    def onLoginSuccessed(self, *args, **kwargs):    
        self.loginSuccessed.emit()

    def onErrorExcepted(self, type_, info, *args, **kwargs):    
        self.errorExcepted.emit(info)
            
    def onPasscodeChecked(self, *args, **kwargs):        
        self.passcodeChecked.emit()
        
    @QtCore.pyqtSlot(result="QVariant")    
    def trainModel(self):
        return self._trainModel
    
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
    def selectPassengerModel(self):
        return self._selectPassengerModel
    
    @QtCore.pyqtSlot(result="QVariant")
    def userHistoryModel(self):
        return self._userHistoryModel
    
    @QtCore.pyqtSlot()
    def requestPassengers(self):
        self._poster.request_passengers()
    
    @QtCore.pyqtSlot(str, str, str)
    def queryTrains(self, fromStation, toStation, date):
        self._poster.query_tickets(fromStation, toStation, date)
        
    @QtCore.pyqtSlot("QVariant", str, "QVariant", str)    
    def grabTickets(self, train, date, passengers, seat_type):
        self._poster.grab_tickets(train, date, passengers, seat_type)
        
    @QtCore.pyqtSlot(str)
    def submitTickets(self, code):
        self._poster.submit_tickets(code)
        
    @QtCore.pyqtSlot("QVariant")    
    def test(self, item):
        self.grabTickets(item, "2013-01-31", self._selectPassengerModel.getAll(), 1)
        

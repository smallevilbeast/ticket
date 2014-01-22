#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime    
from PyQt5 import QtCore, QtWidgets, QtGui

from utils.xdg import get_gui_file
from gui.base import BaseView
from gui.controls import PosterControl
from gui.cookies import NetworkManagerFactory
from gui.calendar import Calendar
from gui import signals as guiSignals

networkManagerFactory = NetworkManagerFactory()

class Instance(BaseView):
    
    calendarClicked = QtCore.pyqtSignal("QVariant")
    calendarChanged = QtCore.pyqtSignal(str)
    mousePressed = QtCore.pyqtSignal(QtCore.QPointF)
    focusLosed =QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(Instance, self).__init__(parent)
        
        self.setTitle("抢票助手")
        self.setIcon(QtGui.QIcon(":/images/common/logo.png"))
        
        QtWidgets.qApp.focusWindowChanged.connect(self.onFocusWindowChanged)
        guiSignals.calendar_date_changed.connect(self.onCalendarDateChanged)
        self._calendar = Calendar()
        self._calendar.calendar.clicked.connect(self.onCalendarActivated)
        self._calendar.calendar.selectionChanged.connect(self.onCalendarSelectionChanged)
        now = datetime.now()
        self._calendar.calendar.setMinimumDate(QtCore.QDate(now.year, now.month, now.day))
        self.engine().setNetworkAccessManagerFactory(networkManagerFactory)
        self._posterControl = PosterControl(self)
        self.setContextProperty("Poster", self._posterControl)        
        self.setSource(QtCore.QUrl.fromLocalFile(get_gui_file("qml", 'Main.qml')))

        
    @QtCore.pyqtSlot()    
    def closeWindow(self):
        self.hide()
        QtWidgets.qApp.quit()
    
    @QtCore.pyqtSlot(int, int)
    def showCalendar(self, x, y):
        globalPos = self.mapToGlobal(QtCore.QPoint(x, y))
        self._calendar.move(globalPos)
        self._calendar.show()
        self._calendar.activateWindow()
        
    @QtCore.pyqtSlot(result=str)    
    def today(self):
        return self._calendar.calendar.selectedDate().toString("yyyy-MM-dd")
        
    def onFocusWindowChanged(self, win):    
        if  win.__class__.__name__   != "QWindow":
            self._calendar.hide()
        if win is None:    
            self.focusLosed.emit()
            
    def onCalendarActivated(self, d):        
        # self.calendarClicked.emit(d)
        self._calendar.hide()
        
    def onCalendarDateChanged(self, date, *args, **kwargs):
        self._calendar.calendar.setSelectedDate(date)
        
    def onCalendarSelectionChanged(self):    
        self.calendarChanged.emit(self._calendar.calendar.selectedDate().toString("yyyy-MM-dd"))
        
    def mousePressEvent(self, event):    
        self.mousePressed.emit(QtCore.QPointF(event.x(), event.y()))
        return super(Instance, self).mousePressEvent(event)

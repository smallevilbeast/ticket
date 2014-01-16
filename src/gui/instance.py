#! /usr/bin/env python
# -*- coding: utf-8 -*-
    
from PyQt5 import QtCore, QtWidgets

from utils.xdg import get_gui_file
from gui.base import BaseView
from gui.controls import PosterControl
from gui.cookies import NetworkManagerFactory
from gui.calendar import Calendar

networkManagerFactory = NetworkManagerFactory()

class Instance(BaseView):
    
    calendarClicked = QtCore.pyqtSignal(str)
    mousePressed = QtCore.pyqtSignal(QtCore.QPointF)
    focusLosed =QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(Instance, self).__init__(parent)
        QtWidgets.qApp.focusWindowChanged.connect(self.onFocusWindowChanged)
        self._calendar = Calendar()
        self._calendar.calendar.clicked.connect(self.onCalendarActivated)
        
        self.engine().setNetworkAccessManagerFactory(networkManagerFactory)
        self._posterControl = PosterControl(self)
        self.setContextProperty("Poster", self._posterControl)        
        self.setSource(QtCore.QUrl.fromLocalFile(get_gui_file("qml", 'Main.qml')))
        
    @QtCore.pyqtSlot()    
    def closeWindow(self):
        pass
    
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
        self.calendarClicked.emit(d.toString("yyyy-MM-dd"))
        self._calendar.hide()
        
    def mousePressEvent(self, event):    
        self.mousePressed.emit(QtCore.QPointF(event.x(), event.y()))
        return super(Instance, self).mousePressEvent(event)
    

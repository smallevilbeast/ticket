#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from gui.window import DWindow

class Calendar(DWindow):
    
    def __init__(self, parent=None):
        super(Calendar, self).__init__(parent)
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        layout = QtWidgets.QVBoxLayout(self)
        self.calendar = QtWidgets.QCalendarWidget(self)
        layout.addWidget(self.calendar)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

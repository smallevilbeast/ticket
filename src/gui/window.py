#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2014 Deepin, Inc.
#               2011 ~ 2014 Hou ShaoHui
# 
# Author:     Hou ShaoHui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5 import QtGui, QtWidgets, QtCore
from gui.common import disableAntialias, setObjectTransparent
        
class DWindow(QtWidgets.QWidget):        
    
    def __init__(self, parent=None):
        super(DWindow, self).__init__(parent)
        
        # transparent
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        setObjectTransparent(self)
        # self.setStyleSheet("background: transparent; border: none;")
        self.borderMargin = 2
        self.contentMargin = 1
        self.fullMargin = self.borderMargin + self.contentMargin
        self.setContentsMargins(self.fullMargin, self.fullMargin, self.fullMargin+1, self.fullMargin+1)
        
        # renders
        self.pix = QtGui.QPixmap()
        
        
    def paintEvent(self, event):    
        painter = QtGui.QPainter(self)
        boundRect = self.rect().adjusted(self.borderMargin, self.borderMargin, -self.borderMargin*2, -self.borderMargin*2)
        
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform 
                            | QtGui.QPainter.TextAntialiasing)

        if not self.pix.isNull():
            painter.save()
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(boundRect), 3.0, 3.0)
            painter.setClipPath(path)
            painter.drawPixmap(boundRect, self.pix)
            painter.restore()
       
        with disableAntialias(painter):
            # draw black border
            pen = QtGui.QPen(QtGui.QColor(30, 30, 30, 255*0.6), 1)
            painter.setPen(pen)
            painter.drawRoundedRect(QtCore.QRectF(boundRect), 3.0, 3.0)
            
            # draw blank border
            pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 255*0.35), 1)
            painter.setPen(pen)
            rect = boundRect.adjusted(1, 1, -1, -1)
            painter.drawRoundedRect(QtCore.QRectF(rect), 3.0, 3.0)
        
    def setBackgroundPixmap(self, image):    
        self.pix = QtGui.QPixmap(image)
        self.update()
        


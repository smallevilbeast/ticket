#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtQuick, QtCore
        
class BaseView(QtQuick.QQuickView):
    
    def __init__(self, parent=None):
        super(BaseView, self).__init__(parent)
        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        surface_format = QtGui.QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)
        self.setColor(QtGui.QColor(0, 0, 0, 0))
        self.setFormat(surface_format)
        self.setFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.Window)
        self.root_context = self.rootContext()        
        self.setContextProperty("windowView", self)        
        
    setContextProperty = property(lambda self: self.root_context.setContextProperty)    
    
    @QtCore.pyqtSlot(result="QVariant")
    def getCursorPos(self):
        return QtGui.QCursor.pos()

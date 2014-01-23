#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.platform == "win32":
    reload(sys)
    sys.setdefaultencoding('gbk')

import os
from PyQt5 import QtCore
if os.name == 'posix':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True) 
    
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import logging
logging.basicConfig(level=logging.DEBUG) # change to 'DEBUG' to see more
#logging.basicConfig(level=logging.ERROR) # change to 'DEBUG' to see more

from PyQt5 import QtWidgets, QtGui
import gui.resource_rc
from gui.instance import Instance


if __name__ == "__main__":
    import sys
    import db
    db.models.init_db()
    app = QtWidgets.QApplication(sys.argv)
    font = QtGui.QFont()
    font.setFamily(font.defaultFamily())
    font.setPixelSize(12)
    app.setFont(font)
    win = Instance()
    win.show()
    sys.exit(app.exec_())


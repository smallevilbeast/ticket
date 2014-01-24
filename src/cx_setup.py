#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from cx_Freeze import setup, Executable


try:
    # delete previous build
    if os.access('./build', os.F_OK):
        shutil.rmtree('./build')
    if os.access('./dist', os.F_OK):
        shutil.rmtree('./dist')
except:
    pass

base = None
include_files = None

if sys.platform == "win32":
    base = "Win32GUI"
    PYQT5_DIR = "C:/Python27/lib/site-packages/PyQt5"
    include_files = [
        "data/station_names.txt",
        "gui/images/",
        "gui/qml/",
        (os.path.join(PYQT5_DIR, "plugins", "iconengines"), "iconengines"),
        (os.path.join(PYQT5_DIR, "qml", "QtQuick.2"), "QtQuick.2"),
        (os.path.join(PYQT5_DIR, "qml", "QtQuick"), "QtQuick"),
        (os.path.join(PYQT5_DIR, "qml", "QtGraphicalEffects"), "QtGraphicalEffects"),
    ]

setup(
    name="EVTicket",
    version="0.9",
    description="EVTicket抢票助手",
    author="evilbeast",
    author_email="houshao55@gmail.com",
    options={"build_exe": {"includes": ["atexit", "sip","PyQt5.QtCore","PyQt5.QtGui","requests","PyQt5.QtWidgets",
                                        "PyQt5.QtNetwork","PyQt5.QtOpenGL", "PyQt5.QtQml", "PyQt5.QtQuick"],
                           "include_files": include_files,
                           "excludes" : ['Tkinter'],
                           # "optimize" : 2,
                           # "compressed" : True,
                           "include_msvcr" : True,
                       }},
    executables=[
        Executable(script="main.py",
                   targetName="EVTicket.exe",
                   icon= "gui/images/common/logo.ico",
                   base=base)
    ]
)
   

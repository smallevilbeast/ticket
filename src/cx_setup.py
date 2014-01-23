#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"
    
setup(
    name="EVTicket",
    version="0.9",
    description="EVTicket抢票助手",
    author="evilbeast",
    author_email="houshao55@gmail.com",
    options={"build_exe": {"includes": ["sip","PyQt5.QtCore","PyQt5.QtGui","requests","PyQt5.QtWidgets",
                                        "PyQt5.QtNetwork","PyQt5.QtOpenGL", "PyQt5.QtQml", "PyQt5.QtQuick"],
                           "include_files": ["data/station_names.txt", "gui/images/", "gui/qml/"],
                           "excludes" : ['Tkinter'],
                       }},
    executables=[
        Executable(script="main.py",
                   targetName="EVticket.exe",
                   icon= "gui/images/common/logo.ico",
                   base=base)
    ]
)
   

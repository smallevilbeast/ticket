#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtQml
from gui.popup import PopupItem

QtQml.qmlRegisterType(PopupItem, "DGui", 1, 0, "PopupItem")

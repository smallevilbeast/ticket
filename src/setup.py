#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from distutils.core import setup
from glob import glob



try:
    # delete previous build
    if os.access('./build', os.F_OK):
        shutil.rmtree('./build')
    if os.access('./dist', os.F_OK):
        shutil.rmtree('./dist')
except:
    pass


if sys.platform.startswith("win"):
    
    # import struct
    # bitness = struct.calcsize("P") * 8    
    
    PYQT5_DIR = r"C:\Python27\Lib\site-packages\PyQt5"
    
    try:
        import py2exe
    except ImportError:
        raise RuntimeError, "Cannot import py2exe"    
    
    data_files = [
        ("data\station_names.txt"),
        ("iconengines", glob(PYQT5_DIR + r'\plugins\iconengines\*.dll')),
        ("imageformats", glob(PYQT5_DIR + r'\plugins\imageformats\*.dll'))
    ]
    
    setup(windows=[{"script" : "main.py"}],
          zipfile=None,
          data_files=data_files,
          options={"py2exe" : {
              "includes" : "sip",
              "dll_excludes" : ["msvcp110.dll"],
              "optimize": 1,              
          }}
    )

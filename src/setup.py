#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import glob
import fnmatch

from distutils.core import setup

VERSION = "0.9"


try:
    # delete previous build
    if os.access('./build', os.F_OK):
        shutil.rmtree('./build')
    if os.access('./dist', os.F_OK):
        shutil.rmtree('./dist')
except:
    pass


def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)

def find_data_files(srcdir, *wildcards, **kw):
    
    def walk_helper(arg, dirname, files):
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)
                
                if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                    names.append(filename)
            if names:
                path = os.path.dirname(srcdir) + os.path.sep
                if path != os.path.sep:
                    d = dirname.replace(path, '')
                else:
                    d = dirname
                print path, dirname, d
                lst.append( (d, names ) )
 
    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards), srcdir, [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list

if sys.platform.startswith("win"):
    
    # import struct
    # bitness = struct.calcsize("P") * 8
    
    PYQT5_DIR = "C:\\Python27\\lib\\site-packages\\PyQt5"
    
    try:
        import py2exe
    except ImportError:
        raise RuntimeError, "Cannot import py2exe"    
    
    data_files = []
    data_files_args = [
        ("gui", ("*.png", "*.jpg", "*.qml", "*.js", "*.ico")),
        ("data", ("*.txt",)),
        (os.path.join(PYQT5_DIR, "plugins", "iconengines"), ("*.dll",)),
        (os.path.join(PYQT5_DIR, "plugins", "platforms"), ("*.dll",)),
        (os.path.join(PYQT5_DIR, "plugins", "imageformats"), ("*.dll",)),
        (os.path.join(PYQT5_DIR, "plugins", "PyQt5"), ("*.dll",)),
        (os.path.join(PYQT5_DIR, "qml", "QtQuick.2"), ("*",)),
        (os.path.join(PYQT5_DIR, "qml", "QtQuick"), ("*",)),
        (os.path.join(PYQT5_DIR, "qml", "QtGraphicalEffects"), ("*",)),
    ]
    
    for srcdir, wildcards in data_files_args:
        data_files.extend(find_data_files(srcdir, *wildcards))
        
    setup(windows=[{"script" : "main.py",
                    "icon_resources": [(1, 'gui\\images\\common\\logo.ico')]
                    }],
          zipfile=None,
          data_files=data_files,
          options={"py2exe" : {
              "includes" : ["sip", "PyQt5.QtQml", "PyQt5.QtQuick"],
              "optimize": 1,              
             # "compressed" : True,
              "dll_excludes": ["MSVCP100.dll", "MSVCP90.dll", "w9xpopen.exe"],
             # "bundle_files": 2,
          }},
          version=VERSION,
          description="12306抢票助手".decode('utf-8'),
          name="EVTicket"
    )

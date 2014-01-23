#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import sys
import time

from utils import common


PROGRAM_NAME = "ticket"

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or \
            os.path.join(_home, '.cache')

if hasattr(sys, 'frozen'):
    program_dir = os.path.dirname(os.path.realpath(sys.executable))
else:
    program_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    
def get_cache_file(path):
    ''' get cache file. '''
    cachefile = os.path.join(xdg_cache_home, PROGRAM_NAME, path)
    cachedir = os.path.dirname(cachefile)
    if not os.path.isdir(cachedir):
        os.makedirs(cachedir)
    return cachefile    

def get_gui_file(*paths):
    return os.path.join(program_dir, "gui", *paths)


def generate_time_md5():
    t = str(time.time())
    return common.get_md5(t)

def get_code_dir():
    d = os.path.join(xdg_cache_home, PROGRAM_NAME, "codes")
    if not os.path.isdir(d):
        os.makedirs(d)
    return d    

def get_uuid_code_path():
    path = os.path.join(get_code_dir(), generate_time_md5())
    while os.path.exists(path):
        path = os.path.join(get_code_dir(), generate_time_md5())
    return path    

def get_cookie_file(username):
    return get_user_file(username, "cookies.txt")

def get_user_file(username, filename):
    d = os.path.join(xdg_cache_home, PROGRAM_NAME, common.get_md5(username))
    if not os.path.isdir(d):
        os.makedirs(d)
    return os.path.join(d, filename)    

def get_data_file(name):
    return os.path.join(program_dir, "data", name)

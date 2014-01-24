#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import time
import random
import string
import hashlib

import threading
from functools import wraps


try:
    import simplejson as json
except ImportError:    
    import json
    
from utils.six.moves import xrange
    
def parse_json(raw):
    try:
        data = json.loads(raw)
    except:    
        try:
            data = eval(raw, type("Dummy", (dict,), dict(__getitem__=lambda s,n: n))())
        except:    
            data = {}
    return data    
    

def timestamp():
    return int(time.time() * 1000)


def get_random_t():
    return random.random()

def radix(n, base=36):
    digits = string.digits + string.lowercase
    def short_div(n, acc=list()):
        q, r = divmod(n, base)
        return [r] + acc if q == 0 else short_div(q, [r] + acc)
    return ''.join(digits[i] for i in short_div(n))

def timechecksum():
    return radix(timestamp())

def quote(s):
    if isinstance(s, unicode):
        s = s.encode("gbk")
    else:    
        s = unicode(s, "utf-8").encode("gbk")
    return urllib.quote(s)    

def unquote(s):
    return urllib.unquote(s)

def get_md5(chars):
    if isinstance(chars, unicode):
        chars = chars.encode("utf-8")
    return hashlib.md5(chars).hexdigest()


def format_size(num, unit='B'):
    next_unit_map = dict(B="K", K="M", M="G", G="T")
    if num > 1024:
        return format_size(num/1024, next_unit_map[unit])
    if num == 0:
        return "0%s  " % unit   # padding
    if unit == 'B':
        return "%.0f%s" % (num, unit)
    return "%.1f%s" % (num, unit)

def get_random_string(length=6):
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for x in xrange(length))

def threaded(f):
    """
        A decorator that will make any function run in a new thread
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=f, args=args, kwargs=kwargs)
        t.setDaemon(True)
        t.start()

    return wrapper


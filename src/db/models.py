#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import logging
import traceback

from contextlib import contextmanager

from utils import xdg
from utils import common
from utils import peewee as pw
from db.base import Model
from db import signals
from core import signals as core_signals
from core.poster import poster
from dispatch import receiver


logger = logging.getLogger('models.Model')
common_db = pw.SqliteDatabase(None, check_same_thread=False, threadlocals=True)
user_db = pw.SqliteDatabase(None, check_same_thread=False, threadlocals=True)

VERSION = "1"
COMMON_DB_INITED = False

@contextmanager
def disable_auto_commit(db):
    db.set_autocommit(False)
    try:
        yield
    except Exception:
        traceback.print_exc(file=sys.stdout)
    else:
        db.commit()
    finally:
        db.set_autocommit(True)

class BaseUserModel(Model):

    class Meta:
        database = user_db
        
class BaseCommonModel(Model):        
    
    class Meta:
        database = common_db
        
class Station(BaseCommonModel):
    jian = pw.CharField()
    quan = pw.CharField()
    telecode = pw.CharField()
    name = pw.CharField()
    
    class Meta:
        db_table = "ticket_stations"
        indexes = (
            # create a non-unique
            (('jian', 'name', 'telecode'), False),
        )        
        
class UserHistory(BaseCommonModel):
    username = pw.CharField(unique=True, index=True)
    password = pw.CharField()
    remember = pw.BooleanField(default=True)
    
    class Meta:
        db_table = "ticket_user_history"
        
class Passenger(BaseUserModel):        
    code = pw.CharField(unique=True, index=True)
    passenger_name = pw.CharField()
    sex_code = pw.CharField()
    sex_name = pw.CharField()
    born_date = pw.CharField()
    country_code = pw.CharField()
    passenger_id_type_code = pw.CharField()
    passenger_id_type_name = pw.CharField()
    passenger_id_no = pw.CharField()
    passenger_type = pw.CharField()
    passenger_flag = pw.CharField()
    passenger_type_name = pw.CharField()
    mobile_no = pw.CharField()
    phone_no = pw.CharField()
    email = pw.CharField()
    address = pw.CharField()
    postalcode = pw.CharField()
    first_letter = pw.CharField()
    recordCount = pw.CharField()
    
    class Meta:
        db_table = "ticket_passengers"
        
class MonitorHistory(BaseUserModel):
    passenger_codes = pw.CharField()
    from_station = pw.CharField()
    to_station = pw.CharField()
    date = pw.CharField()
    trains = pw.CharField()
    seats = pw.CharField()
    
    class Meta:
        db_table = "ticket_moniter"
        
class StationHistory(BaseUserModel):        
    name = pw.CharField()
    telecode = pw.CharField()
    
    class Meta:
        db_table = "ticket_station_history"
        
def create_common_tables():
    Station.create_table()
    UserHistory.create_table()
    
def create_user_tables():    
    Passenger.create_table()
    MonitorHistory.create_table()
    StationHistory.create_table()
    
def insert_station_data():    
    f = xdg.get_data_file("station_names.txt")
    with open(f) as fp:
        content = fp.read().decode("utf-8").strip("\n")
        lines = content.split("@")
        with disable_auto_commit(common_db):
            for line in lines:
                if not line.strip():
                    continue
                jian, name, telecode, quan, _, _ = tuple(line.split("|"))
                params = dict(name=name, telecode=telecode, quan=quan, jian=jian)
                Station.create(**params)
                
def _init_common_db():
    global COMMON_DB_INITED
    db_file = xdg.get_cache_file("ticket_common_{0}.db".format(VERSION))
    common_db.init(db_file)
    created = False
    if not os.path.exists(db_file):
        common_db.connect()
        create_common_tables()
        insert_station_data()
        created = True
    signals.db_init_finished.send(sender=common_db, created=created)        
    COMMON_DB_INITED = True

    
@receiver(core_signals.login_successed)
@common.threaded
def _init_user_db(sender, username, *args, **kwargs):
    db_file = xdg.get_user_file(username, "dat_{0}.db".format(VERSION))
    user_db.init(db_file)
    created = False
    if not os.path.exists(db_file):
        user_db.connect()
        create_user_tables()
        poster.request_passengers()
        created = True
    signals.db_init_finished.send(sender=user_db, created=created)    
    
@receiver(core_signals.passengers_received)    
def _update_passengers(sender, passengers, *args, **kwargs):
    with disable_auto_commit(user_db):
        for p in passengers:
            code = p.get("code", None)
            if not code:
                continue
            try:
                Passenger.get(code=code)
            except Passenger.DoesNotExist:
                Passenger.create(**p)
    logger.debug("-- save passengers to db")        
    
@receiver(core_signals.login_successed)    
def _add_to_history(sender, username, password, *args, **kwargs):
    try:
        obj = UserHistory.get(username=username)
    except UserHistory.DoesNotExist:    
        UserHistory.create(username=username, password=password)
    else:    
        if obj.password != password:
            obj.password = password
            obj.save(update_fields=['password'])
                
@common.threaded                
def init_db():    
    _init_common_db()
    logger.info("-- initial database completed")    
    

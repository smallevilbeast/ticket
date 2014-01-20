#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import logging
import requests
import re

from utils.six.moves import http_cookiejar as cookielib

from core import signals 
from utils import xdg
from utils import common
from utils import six
from collections import OrderedDict
from utils.six.moves.urllib.parse import unquote
from datetime import datetime

logger = logging.getLogger("Poster")

SEAT_TYPE = OrderedDict()
SEAT_TYPE['商务座'] = "9"
SEAT_TYPE['特等座'] = "P"
SEAT_TYPE['一等座'] = "M"
SEAT_TYPE['二等座'] = "O"
SEAT_TYPE['高级软卧'] = "5"
SEAT_TYPE['软卧'] = "4"
SEAT_TYPE['硬卧'] = "3"
SEAT_TYPE['软座'] = "2"
SEAT_TYPE['硬座'] = "1"
SEAT_TYPE['无座'] = "1"
SEAT_TYPE['其他'] = ""

JSON_SEAT = {
    "gr_num" : "高级软卧",
    "qt_num" : "其他",
    "rw_num" : "软卧",
    "rz_num" : "软座",
    "tz_num" : "特等座",
    "wz_num" : "无座",
    "yw_num" : "硬卧",
    "yz_num" : "硬座",
    "ze_num" : "二等座",
    "zy_num" : "一等座",
    "swz_num" : "商务座",
}

REVERSAL_JSON_SEAT = dict((v, k) for k,v in six.iteritems(JSON_SEAT))

class Poster(object):
    
    def __init__(self, username=None, passwd=None):
        self._username = username
        self._passwd = passwd
        
        self._headers = {
            "User-Agent" : "Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0;)",
        }
        cookie_jar = cookielib.LWPCookieJar()        
        self._session = requests.Session()        
        self._session.cookies = cookie_jar
        self._session.headers = self._headers
        self._session.verify = False
        self._order_infos = dict()
        
    @common.threaded    
    def check_login(self, username=None, passwd=None):
        passwd = passwd or self._passwd                        
        username = username or self._username
        if not passwd and not username:
            signals.error_excepted.send(sender=self, type_="login", info="请输入完整登录信息")
            return
        
        self._username = username
        self._passwd = passwd
        
        cookie_file = xdg.get_cookie_file(username)
        self._session.cookies.filename = cookie_file
        
        if os.path.isfile(cookie_file):
            # load cookies
            self._session.cookies.load(ignore_discard=True, ignore_expires=True)
            if self.user_logined:    
                logger.info("-- account {0} login success [cookies]".format(username))
                signals.login_successed.send(sender=self, username=self._username, password=self._passwd)
                return True
            else:
                self._session.cookies.clear()
                
        self.new_passcode()
            
    @common.threaded    
    def login(self, rand_code):    
        data = {"loginUserDTO.user_name": self._username, "userDTO.password" : self._passwd, "randCode" : rand_code}
        ret = self._session.post("https://kyfw.12306.cn/otn/login/loginAysnSuggest", data=data).json()
        login_check = ret.get("data", {}).get("loginCheck", "N")
        if login_check == "Y":
            logger.info("-- account {0} login success [requests]".format(self._username))
            logger.debug("-- save cookies to file")
            self._session.cookies.save(ignore_discard=True, ignore_expires=True)
            
            # emit login_successed signals.
            signals.login_successed.send(sender=self, username=self._username, password=self._passwd)
            
            return True
        
        message = ";".join(ret.get("messages", []))
        logger.info("-- login failed!!! {0}".format(message))
        signals.error_excepted.send(sender=self, type_="login", info=message)
                        
    @common.threaded        
    def new_passcode(self, module="login", rand="sjrand"):
        data = dict(module=module, rand=rand)
        ret =  self._session.get("https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew", params=data, stream=True)
        
        path = xdg.get_uuid_code_path()
        with open(path, 'wb') as fd:
            for chunk in ret.iter_content(2048):
                fd.write(chunk)
        signals.passcode_newed.send(sender=self, module=module, url=path, ran_code=rand)            
    
    @common.threaded    
    def check_passcode(self, rand_code, module, rand="sjrand"):
        data = dict(randCode=rand_code, rand=rand)
        ret = self._session.post("https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn", data=data).json()
        if ret.get("data", "N") == "Y":
            signals.passcode_checked.send(sender=self, module=module, value=True)
        else:    
            self.new_passcode()
            
    def order_passcode(self):        
        self.new_passcode(module="passenger", rand="randp")
    
    @common.threaded    
    def request_passengers(self):
        ret = self._session.post("https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs").json()
        status = ret.get("status", False)
        if status:
            passengers = ret.get("data", {}).get("normal_passengers", [])
            logger.info("-- received {0} passengers".format(len(passengers)))
            signals.passengers_received.send(sender=self, passengers=passengers)
            signals.error_excepted.send(sender=self, type_="query", info="联系人信息已经刷新")
        
    @property    
    def user_logined(self):    
        data = {"_json_att" : ""}
        ret = self._session.post("https://kyfw.12306.cn/otn/login/checkUser", data=data).json()
        return ret.get("data", {}).get("flag", False)
    
    def get_station_names(self):
        ret = self._session.get("https://kyfw.12306.cn/otn/resources/js/framework/station_name.js")
        return ret
        
    @common.threaded    
    def query_trains(self, from_station, to_station, date, sender=None):    
        if not from_station or not to_station or not date:
            signals.error_excepted.send(sender=self, type_="query", info="请输入完整信息")
            return
        
        if sender is None: 
            sender = self
            
        _data = OrderedDict()
        _data['purpose_codes'] = "ADULT"
        _data['queryDate'] = date
        _data['from_station'] = from_station
        _data['to_station'] = to_station
        
        url = "https://kyfw.12306.cn/otn/lcxxcx/query"
        ret = self._session.get(url, params=_data).json()
        if ret == -1:
            signals.error_excepted.send(sender=self, type_="query", info="查询错误, 请重试")
            return 
        data = ret.get("data", {})
        flag = data.get("flag", False)
        if flag:
            signals.query_trains_completed.send(sender=sender, data=data.get("datas"))
        else:    
            message = data.get("message", "")
            signals.error_excepted.send(sender=self, type_="query", info=message)
            
    @common.threaded        
    def query_tickets(self, from_station, to_station, date, sender=None, sendError=True):        
        if not from_station or not to_station or not date:
            signals.error_excepted.send(sender=self, type_="query", info="请输入完整信息")
            return
        
        if sender is None: 
            sender = self
        
        url = "https://kyfw.12306.cn/otn/leftTicket/query"
        data = OrderedDict()
        data['leftTicketDTO.train_date'] = date
        data['leftTicketDTO.from_station'] = from_station
        data['leftTicketDTO.to_station'] = to_station
        data['purpose_codes'] = "ADULT"
        ret = self._session.get(url, params=data).json()
        if ret == -1:
            signals.error_excepted.send(sender=self, type_="query", info="查询错误, 请重试")
            return 
        
        ret_data = ret.get("data", [])
        if not ret_data:
            ret_data = None            
            if sendError:    
                msg = "".join(ret.get("messages", []))
                if not msg.strip():
                    msg = "没有查询到结果, 请注意购票日期"
                signals.error_excepted.send(sender=self, type_="query", info=msg)

        signals.query_tickets_completed.send(sender=sender, data=ret_data)
            
    @staticmethod
    def re_search(pattern, content):
        try:
            return re.search(pattern, content).group(1)
        except AttributeError:    
            return ""
        
    @staticmethod    
    def parse_train_date(date):
        week_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        month_name = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
        y, m, d = map(int, date.split("-"))
        weekday = datetime(y, m, d).weekday()

        # fix c locale 
        return "{0} {1} {2} {3} 00:00:00 GMT+0800 (CST)".format(week_name[weekday], month_name[m-1], d, y)
    
    @staticmethod
    def parse_passenger_ticket(passengers, seat_type):
        # 席位(3 硬卧，1 硬座)，0,1，姓名，1(第一个选项，第二代身份证)，身份证号，电话，N                
        results = []
        for p in passengers:
            pstr = "{0},0,1,{1},{2},{3},{4},N".format(seat_type, p.passengerName,
                                                      p.passengerIdTypeCode, p.passengerIdNo, p.mobileNo)
            results.append(pstr)
        return "_".join(results)    
    
    @staticmethod
    def parse_old_passenger(passengers):
        # 姓名，1，身份证号，1_        
        results = []
        for p in passengers:
            pstr = "{0},{1},{2},1_".format(p.passengerName, p.passengerIdTypeCode, p.passengerIdNo)
            results.append(pstr)
        return "".join(results)    
        
    @common.threaded
    def grab_tickets(self, train, date, passengers, seat_type):
        if not self.submit_order_request(train):
            signals.query_tickets_failed.send(sender=self)
            return False
        
        ret = self.confirm_passenger()
        if not ret:
            signals.query_tickets_failed.send(sender=self)
            return False
        
        self._order_infos.clear()
        self._order_infos.update(ret)    # update token
        self._order_infos['passengerTicketStr'] = self.parse_passenger_ticket(passengers, seat_type)
        self._order_infos['oldPassengerStr'] = self.parse_old_passenger(passengers)
        self._order_infos['train'] = train
        self._order_infos['seat_type'] = seat_type
        self._order_infos['dateStr'] = self.parse_train_date(date)
        self._order_infos['date'] = date
        
        # request new passcode
        self.order_passcode()
        
    @common.threaded    
    def submit_tickets(self, code):    
        self._order_infos["randCode"] = code
        
        ret = self.check_order_info()
        if not ret:
            signals.grab_tickets_failed.send(sender=self)
            return
        
        ret = self.get_quque_count()
        if not ret:
            signals.grab_tickets_failed.send(sender=self)
            return
        
        ret = self.confirm_order()
        if not ret:
            signals.grab_tickets_failed.send(sender=self)
            return
        
        signals.grab_tickets_successed.send(sender=self)
    
    def submit_order_request(self, train):        
        url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        data = OrderedDict()
        data['secretStr'] = unquote(train.secretStr.encode("utf-8"))
        data['train_date'] = train.startTrainDate 
        data['back_train_date'] = train.startTrainDate
        data['tour_flag'] = "dc"
        data['purpose_codes'] = "ADULT"
        data['query_from_station_name'] = train.fromStationName
        data['query_to_station_name'] = train.toStationName
        data['undefined'] = ""
        ret = self._session.post(url, data=data).json()
        status = ret.get("status", False)
        if not status:
            messages = "提交订单请求失败: {0}".format("".join(ret.get("messages", [])))
            signals.error_excepted.send(sender=self, type_="order", info=messages)
        return status    
    
    def confirm_passenger(self):    
        url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        data = {"_json_att" : ""}
        ret = self._session.post(url, data=data).text
        submit_token = self.re_search("var globalRepeatSubmitToken = '([a-z0-9]+)';", ret)
        key_check_isChange = self.re_search("'key_check_isChange':'([A-Z0-9]+)'", ret)
        infos = dict()
        infos["REPEAT_SUBMIT_TOKEN"] = submit_token
        infos["key_check_isChange"] = key_check_isChange
        return infos
                
    def check_order_info(self):    
        url = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        data = OrderedDict()
        data['cancel_flag'] = 2
        data['bed_level_order_num'] = "000000000000000000000000000000"
        data['passengerTicketStr'] = self._order_infos['passengerTicketStr']
        data['oldPassengerStr'] = self._order_infos['oldPassengerStr']
        data['tour_flag'] = "dc"
        data['randCode'] = self._order_infos['randCode']
        data['_json_att'] = ""
        data['REPEAT_SUBMIT_TOKEN'] = self._order_infos["REPEAT_SUBMIT_TOKEN"]
        ret = self._session.post(url, data=data).json()
        submit_status = ret.get('data', {}).get("submitStatus", False)
        if not submit_status:
            message = "检测订单信息: " + "".join(ret.get("messages", []))
            signals.error_excepted.send(sender=self, type_="order", info=message)
        return submit_status
        
    def get_quque_count(self):    
        url = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
        train = self._order_infos['train']
        data = OrderedDict()
        data['train_date'] = self._order_infos['dateStr']
        data['train_no'] = train.trainNo
        data['stationTrainCode'] = train.stationTrainCode
        data['seatType'] = self._order_infos['seat_type']
        data['fromStationTelecode'] = train.fromStationTelecode
        data['toStationTelecode'] = train.toStationTelecode
        data['leftTicket'] = train.ypInfo
        data['purpose_codes'] = "00"
        data['_json_att'] = ""
        data['REPEAT_SUBMIT_TOKEN'] = self._order_infos['REPEAT_SUBMIT_TOKEN']
        ret = self._session.post(url, data=data).json()
        status = ret.get("status", False)
        if not status:
            signals.error_excepted.send(sender=self, type_="order", info="".join(ret.get("messages", [])))
            return False
        ret_data = ret.get("data", {})
        ticket = ret_data.get("ticket", "")
        if not ticket:
            message = "前面已有{0}人在排队".format(ret_data.get("count", 0))
            signals.error_excepted.send(sender=self, type_="order", info=message)
        self._order_infos['leftTicketStr'] = ticket
        return bool(ticket)
    
    def confirm_order(self):    
        url = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        data = OrderedDict()
        data['passengerTicketStr'] = self._order_infos["passengerTicketStr"]
        data['oldPassengerStr'] = self._order_infos['oldPassengerStr']
        data['randCode'] = self._order_infos['randCode']
        data['purpose_codes'] = "00"
        data['key_check_isChange'] = self._order_infos['key_check_isChange']
        data['leftTicketStr'] = self._order_infos['leftTicketStr']
        data['train_location'] = self._order_infos["train"].locationCode
        data['REPEAT_SUBMIT_TOKEN'] = self._order_infos["REPEAT_SUBMIT_TOKEN"]
        ret = self._session.post(url, data=data).json()
        submit_status = ret.get('data', {}).get("submitStatus", False)
        if not submit_status:
            signals.error_excepted.send(sender=self, type_="order", info="确认订单失败: " + "".join(ret.get("messages", [])))
        return submit_status    
        
        
poster = Poster()

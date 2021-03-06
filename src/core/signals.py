#! /usr/bin/env python
# -*- coding: utf-8 -*-

from dispatch import Signal

error_excepted = Signal(providing_args=['type_', 'info'])
passcode_newed = Signal(providing_args=['module', 'url', 'rand_code'])
login_successed = Signal(providing_args=['username', 'password'])
passcode_checked = Signal(providing_args=['module', 'value'])
query_trains_completed = Signal(providing_args=['data'])
query_tickets_completed = Signal(providing_args=['data'])
passengers_received = Signal(providing_args=['passengers'])
grab_tickets_successed = Signal(providing_args=[])
grab_tickets_failed = Signal(providing_args=[])
query_tickets_failed = Signal(providing_args=[])

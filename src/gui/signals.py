#! /usr/bin/env python
# -*- coding: utf-8 -*-



from dispatch import Signal

calendar_date_changed = Signal(providing_args=['date'])

#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2014 Deepin, Inc.
#               2011 ~ 2014 Hou ShaoHui
# 
# Author:     Hou ShaoHui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dispatch import Signal

pre_save = Signal(providing_args=["instance", "created", "update_fields"])
post_save = Signal(providing_args=["instance", "created", "update_fields"])
pre_delete = Signal(providing_args=["instance"])
post_delete = Signal(providing_args=["instance"])
pre_init = Signal(providing_args=["instance"])
post_init = Signal(providing_args=["instance"])
db_init_finished = Signal(providing_args=["created"])

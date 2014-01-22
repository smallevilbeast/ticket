#! /usr/bin/env python
# -*- coding: utf-8 -*-

from utils.peewee import Model as _Model
from db import signals 

class Model(_Model):
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        signals.pre_init.send(sender=self.__class__, instance=self)

    def prepared(self):
        super(Model, self).prepared()
        signals.post_init.send(sender=self.__class__, instance=self)

    def save(self, *args, **kwargs):
        if "update_fields" in kwargs:
            update_fields = kwargs.pop("update_fields")
        else: update_fields = None
        
        created = not bool(self.get_id())
        signals.pre_save.send(sender=self.__class__, instance=self, created=created, update_fields=update_fields)
        super(Model, self).save(*args, **kwargs)
        signals.post_save.send(sender=self.__class__, instance=self, created=created, update_fields=update_fields)
        
    def delete_instance(self, *args, **kwargs):
        signals.pre_delete.send(sender=self.__class__, instance=self)
        super(Model, self).delete_instance(*args, **kwargs)
        signals.post_delete.send(sender=self.__class__, instance=self)


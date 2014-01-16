#! /usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from PyQt5 import QtCore
from utils import six
                
class QPropertyMeta(QtCore.pyqtWrapperType):
    
    def __new__(cls, cls_name, cls_bases, cls_dict):
        super_new = super(QPropertyMeta, cls).__new__
        props = cls_dict.get("__qtprops__", None)
        if props is not None:
            for key, values in six.iteritems(props):
                nty = cls_dict['_nty_'+key] = QtCore.pyqtSignal()
                if isinstance(values, tuple) and len(values) == 2:
                    _type, default = values
                else:    
                    _type = type(values)
                    if _type not in (int, str, bool):
                        _type = "QVariant"
                    default = values
                    
                cls_dict["_"+key] = default
                
                def _get(key):
                    def f(self):
                        return getattr(self, '_'+key)
                    return f
                
                def _set(key):
                    def f(self, value):
                        setattr(self, '_'+key, value)
                        getattr(self, "_nty_"+key).emit()                    
                    return f
                
                set_func = cls_dict['_set_'+key] = _set(key)
                get_func = cls_dict['_get_'+key] = _get(key)
                
                cls_dict[key] = QtCore.pyqtProperty(_type, get_func, set_func, notify=nty)
        return super_new(cls, cls_name, cls_bases, cls_dict)        
                

class QObjectListModel(QtCore.QAbstractListModel):
    
    _roles = {}
    
    def __init__(self, parent=None):
        super(QObjectListModel, self).__init__(parent)
        self._data = []
        
    def roleNames(self):    
        return self._roles
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.size()
    
    def setAll(self, data):
        oldSize = self.size()
        self.beginResetModel()
        self._data = data
        self.endResetModel()
        self.dataChanged.emit(self.index(0), self.index(self.size()-1), [])
        if self.size() != oldSize:
            self.countChanged.emit()
            
    def getAll(self):        
        return self._data
    
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size():
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        for r, name in six.iteritems(self._roles):
            if r == role:
                getattr(item, name, QtCore.QVariant())
        return QtCore.QVariant()        
    
    def append(self, objs):
        if not isinstance(objs, list):
            objs = [ objs ]
        self.beginInsertRows(QtCore.QModelIndex(), self.size(), self.size()+len(objs)-1)    
        self._data.extend(objs)
        self.endInsertRows()
        self.countChanged.emit()
        
    def insert(self, i, objs):    
        if not isinstance(objs, list):
            objs = [ objs ]
        self.beginInsertRows(QtCore.QModelIndex(), i, i+len(objs)-1)    
        for obj in reversed(objs):
            self._data.insert(i, obj)
        self.endInsertRows()    
        self.countChanged.emit()
        
    def replace(self, obj, i=None):    
        if i is None:
            try:
                i = self.indexOf(obj)
            except ValueError:  
                i = None
        if i is None:        
            return
        self._data[i] = obj
        self.dataChanged.emit(self.index(i), self.index(i), [])
        
    def move(self, fromIndex, toIndex):    
        value = toIndex
        if toIndex > fromIndex:
            value += 1
        if not self.beginMoveRows(QtCore.QModelIndex(), fromIndex, fromIndex, QtCore.QModelIndex(), value):
            return
        self._data.insert(toIndex, self._data.pop(fromIndex))
        self.endMoveRows()
        
    def removeAt(self, i, count=1):    
        self.beginRemoveRows(QtCore.QModelIndex(), i, i + count - 1)
        for cpt in range(count):
            self._data.pop(i)
        self.endRemoveRows()
        self.countChanged.emit()
        
    def remove(self, obj):
        if not self.contains(obj):
            raise ValueError("QObjectListModel.remove(obj) : obj not in list")
        self.removeAt(self.indexOf(obj))
        
    def takeAt(self, i):
        self.beginRemoveRows(QtCore.QModelIndex(), i, i)
        obj = self._data.pop(i)
        self.endRemoveRows()
        self.countChanged.emit()
        return obj
    
    @QtCore.pyqtSlot()
    def clear(self):
        if not self._data:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.size() - 1)
        del self._data[:]
        self.endRemoveRows()
        self.countChanged.emit()

    def contains(self, obj):
        return obj in self._data
        
    def indexOf(self, matchObj, fromIndex=0, positive=True):    
        index = self._data[fromIndex:].index(matchObj) + fromIndex
        if positive and index < 0:
            index += self.size()
        return index
    
    def lastIndexOf(self, matchObj, fromIndex=-1, positive=True):
        r = list(self._data)
        r.reverse()
        index = - r[-fromIndex - 1:].index(matchObj) + fromIndex
        if positive and index < 0:
            index += self.size()
        return index
    
    def size(self):
        return len(self._data)
    
    @QtCore.pyqtSlot(result=bool)
    def isEmpty(self):
        return self.size() == 0
    
    @QtCore.pyqtSlot(int, result="QVariant")
    def get(self, i):
        return self._data[i]
    
    def __iter__(self):
        """ Enables iteration over the list of objects. """
        return iter(self._data)

    def __len__(self):
        return self.size()

    def __nonzero__(self):
        return self.size() > 0

    def __getitem__(self, index):
        """ Enables the [] operator """
        return self._data[index]
    
    countChanged = QtCore.pyqtSignal()
    count = QtCore.pyqtProperty(int, size, notify=countChanged)
    
def QPropertyObject():    
    return six.with_metaclass(QPropertyMeta, QtCore.QObject)


class postGui(QtCore.QObject):
    
    throughThread = QtCore.pyqtSignal(object, object)    
    
    def __init__(self, inclass=True):
        super(postGui, self).__init__()
        self.throughThread.connect(self.onSignalReceived)
        self.inclass = inclass
        
    def __call__(self, func):
        self._func = func
        
        @functools.wraps(func)
        def objCall(*args, **kwargs):
            self.emitSignal(args, kwargs)
        return objCall
        
    def emitSignal(self, args, kwargs):
        self.throughThread.emit(args, kwargs)
                
    def onSignalReceived(self, args, kwargs):
        if self.inclass:
            obj, args = args[0], args[1:]
            self._func(obj, *args, **kwargs)
        else:    
            self._func(*args, **kwargs)
            
            
def ObjectWrapper(dictData):    
    class WrapperQuery(six.with_metaclass(QPropertyMeta, QtCore.QObject)):
        __qtprops__ = dictData
        
    return WrapperQuery()    

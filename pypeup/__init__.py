# -*- coding: utf-8 -*-

__all__ = ["DataPipe"]
__author__ = "DboyLiao <qmalliao@gmail.com>"
__license__ = "MIT"
__version__ = ("0", "7")

from ._metaclass import PipeMeta
from functools import wraps
from .exceptions import ExecutionContextError

class DataPipe(object):

    __metaclass__ = PipeMeta

    def __new__(cls, data, *args, **kwargs):
        obj = super(DataPipe, cls).__new__(cls)
        obj.__under_execution_context = False
        return obj

    def __init__(self, data, *args, **kwargs):
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not self.__under_execution_context:
            raise ExecutionContextError("data can not be modified outside of execution of methods.")

        if not isinstance(value, type(self.data)):
            raise TypeError("The data should be of type {}: {} is given.".format(type(self.data), type(value)))
        
        self._data = value

    def register(self, fun):

        @wraps(fun)
        def wrapped(*args, **kwargs):
            
            new_data = fun(self.data, *args, **kwargs)
            self.data = new_data
            return self

        setattr(self, fun.__name__, wrapped)

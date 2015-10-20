# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import collections.abc
import yaml


class Config(collections.abc.Mapping):
    __slots__ = '__data',

    def __init__(self, i):
        self.__data = yaml.safe_load(i)

    def __getitem__(self, key):
        return self.__data.__getitem__(key)

    def __iter__(self):
        return self.__data.__iter__()

    def __len__(self):
        return self.__data.__len__()

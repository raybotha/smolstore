# -*- coding: utf-8 -*-
from typing import Iterable, Mapping, MutableMapping
from .field import Field


class Fields(Mapping):
    def __init__(self, _fields: Iterable[Field] = None, _import: MutableMapping = None):
        if _fields:
            self.__slots__ = {field.name: field for field in _fields}
        elif _import:
            self.__slots__ = {k: Field(_import=_import[v]) for k, v in _import.items()}
        else:
            self.__slots__ = {}

    def __getitem__(self, key):
        return self.__slots__[key]

    def __iter__(self):
        return self.__slots__.__iter__()

    def __len__(self):
        return self.__slots__.__len__()

    def __repr__(self):
        return "Fields(%r)" % self.__slots__

    def __str__(self):
        return self.__slots__.__str__()

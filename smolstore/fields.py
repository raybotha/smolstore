# -*- coding: utf-8 -*-
from typing import Iterable
from typing import Mapping
from typing import MutableMapping

from .field import Field


class Fields(Mapping):
    def __init__(self, _fields: Iterable[Field] = None):
        if not _fields:
            _fields = {}
        self.__dict__ = {field.name: field for field in _fields}

    @classmethod
    def _deserialize(cls, _data: MutableMapping):
        fields = cls()
        fields.__dict__ = {
            field_name: Field._deserialize(field) for field_name, field in _data.items()
        }
        return fields

    def _serialize(self) -> dict:
        return {field_name: field._serialize() for field_name, field in self.__dict__}

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return self.__dict__.__len__()

    def __repr__(self):
        return "Fields(%r)" % self.__dict__

    def __str__(self):
        return self.__dict__.__str__()

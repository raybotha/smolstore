# -*- coding: utf-8 -*-
from typing import Iterable
from typing import MutableMapping
from typing import Sequence
from uuid import uuid4

from .field import Field
from .fields import Fields


class Table(Sequence):
    def __init__(self, _fields: Iterable[Field] = None):
        self._data = {}
        self.fields = Fields(_fields=_fields)

    @classmethod
    def _deserialize(cls, _data: MutableMapping):
        table = cls()
        table._data = _data["_data"]
        table.fields = Fields._deserialize(_data["_fields"])
        return table

    def _serialize(self) -> dict:
        return {"_data": self._data, "_fields": self.fields._serialize()}

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        self._data.__setitem__(key, value)

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def __len__(self):
        return self._data.__len__()

    def insert(self, document):
        key = uuid4().hex
        self.__setitem__(key, document)

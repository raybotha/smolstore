# -*- coding: utf-8 -*-
from threading import Lock
from typing import Iterable, Sequence, MutableMapping
from .field import Field
from .fields import Fields
from uuid import uuid4


class Table(Sequence):
    def __init__(
        self,
        _lock: Lock,
        _import: MutableMapping = None,
        _fields: Iterable[Field] = None,
    ):
        self._lock = _lock
        self._data = _import["_data"] if _import else {}
        self.fields = (
            Fields(_import=_import["_fields"]) if _import else Fields(_fields=_fields)
        )

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __len__(self):
        return self._data.__len__()

    def insert(self, document):
        key = uuid4().hex
        self.__setitem__(key, document)

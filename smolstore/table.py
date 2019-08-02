# -*- coding: utf-8 -*-
from threading import Lock
from typing import Iterable, MutableSequence, MutableMapping
from .field import Field
from .fields import Fields


class Table(MutableSequence):
    def __init__(
        self,
        _lock: Lock,
        _import: MutableMapping = None,
        _fields: Iterable[Field] = None,
    ):
        self._lock = _lock
        self._data = _import["_data"] if _import else []
        self.fields = (
            Fields(_fields=_fields) if _fields else Fields(_import=_import["_fields"])
        )

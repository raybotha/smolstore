# -*- coding: utf-8 -*-
from typing import Iterable
from typing import Iterator
from typing import MutableMapping
from typing import Sequence
from uuid import uuid4

from .field import Field
from .fields import Fields
from .query import ComparisonType
from .query import Query


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

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def __len__(self):
        return self._data.__len__()

    def insert(self, document):
        if not isinstance(document, MutableMapping):
            raise TypeError("Only dict-compatible types are supported")
        key = uuid4().hex
        self._data.__setitem__(key, document)

    def get(self, query: Query) -> Iterator:
        if query.field.indexed:
            document_keys = query.field._get_keys(query.comparison_type, query.value)

            if query.comparison_type == ComparisonType.EQUAL:
                for key in document_keys:
                    yield self._data[key]
            elif query.comparison_type == ComparisonType.NOT_EQUAL:
                for document_key, document in self._data.items():
                    if document_key not in document_keys:
                        yield document
        else:
            for document in self._data.values():
                if document.get(query.field) == query.value:
                    yield document

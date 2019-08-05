# -*- coding: utf-8 -*-
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import MutableMapping
from uuid import uuid4

from .document import Document
from .field import Field
from .fields import Fields
from .query import ComparisonType
from .query import Query


class Table(Iterable):
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

    def __iter__(self):
        for value in self._data.values():
            yield value

    def __len__(self):
        return self._data.__len__()

    def __repr__(self):
        return repr(list(self._data.values()))

    def insert(self, document):
        if not isinstance(document, Mapping):
            raise TypeError("Only dict-compatible types are supported")

        key = uuid4().hex
        document = Document(_table=self, _document_key=key, mapping=document)
        self._data.__setitem__(key, document)

    def upsert(self, document, field):
        raise NotImplementedError

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
            if query.comparison_type == ComparisonType.EQUAL:
                for document in self._data.values():
                    if document.get(query.field.name) == query.value:
                        yield document
            elif query.comparison_type == ComparisonType.NOT_EQUAL:
                for document in self._data.values():
                    if document.get(query.field.name) != query.value:
                        yield document

    def delete(self, query: Query):
        raise NotImplementedError

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
        table.fields = Fields._deserialize(_data["_fields"])
        table._data = {
            key: Document(
                _table=table,
                _document_key=value["_document_key"],
                mapping=value["_data"],
            )
            for key, value in _data["_data"].items()
        }
        return table

    def _serialize(self) -> dict:
        return {
            "_data": {
                key: {"_document_key": document._document_key, "_data": dict(document)}
                for key, document in self._data.items()
            },
            "_fields": self.fields._serialize(),
        }

    def __iter__(self):
        for value in self._data.values():
            yield value

    def __len__(self):
        return self._data.__len__()

    def __repr__(self):
        return "Table(%r)" % list(self._data.values())

    def insert(self, document):
        if not isinstance(document, Mapping):
            raise TypeError("Only dict-compatible types are supported")

        key = uuid4().hex
        document = Document(_table=self, _document_key=key, mapping=document)
        self._data.__setitem__(key, document)

    def upsert(self, document, query, multiple=False):
        for key in self._get_keys(query):
            self._data[key].update(document)
            if multiple is False:
                break

    def _get_keys(self, query: Query) -> Iterator:
        if query.field.indexed:
            if query.comparison_type == ComparisonType.EQUAL:
                for key in query.field._get_keys(ComparisonType.EQUAL, query.value):
                    yield key
            elif query.comparison_type == ComparisonType.NOT_EQUAL:
                equal_keys = query.field._get_keys(ComparisonType.EQUAL, query.value)
                for key in self._data.keys():
                    if key not in equal_keys:
                        yield key
        else:
            if query.comparison_type == ComparisonType.EQUAL:
                for key, document in self._data.items():
                    if document.get(query.field.name) == query.value:
                        yield key
            elif query.comparison_type == ComparisonType.NOT_EQUAL:
                for key, document in self._data.items():
                    if document.get(query.field.name) != query.value:
                        yield key

    def get(self, query: Query) -> Iterator:
        for key in self._get_keys(query):
            yield self._data[key]

    def first(self, query: Query):
        for key in self._get_keys(query):
            return self._data[key]
        return None

    def _delete_document(self, document_key):
        self._data[document_key].clear()
        del self._data[document_key]

    def delete(self, query: Query):
        keys = list(self._get_keys(query))
        for key in keys:
            self._delete_document(key)

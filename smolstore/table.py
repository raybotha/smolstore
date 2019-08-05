# -*- coding: utf-8 -*-
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import MutableMapping
from uuid import uuid4

from .document import Document
from .exceptions import MissingField
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

    def upsert(self, document, field: Field, multiple=False):
        try:
            match_value = document[field.name]
        except KeyError:
            raise MissingField("Specified field does not exist in passed document")

        for key in self._get_keys(field == match_value):
            self._data[key].update(document)
            if multiple is False:
                break

    def _get_keys(self, query: Query) -> Iterator:
        if query.field.indexed:
            document_keys = query.field._get_keys(query.comparison_type, query.value)

            if query.comparison_type == ComparisonType.EQUAL:
                for key in document_keys:
                    yield key
            elif query.comparison_type == ComparisonType.NOT_EQUAL:
                for key, document in self._data.items():
                    if key not in document_keys:
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

    def first(self, query: Query) -> Iterator:
        for key in self._get_keys(query):
            yield self._data[key]
            break
        return None

    def _delete_document(self, document_key):
        self._data[document_key].clear()
        del self._data[document_key]

    def delete(self, query: Query):
        keys = list(self._get_keys(query))
        for key in keys:
            self._delete_document(key)

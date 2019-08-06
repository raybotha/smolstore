# -*- coding: utf-8 -*-
from typing import Iterable
from typing import Iterator
from typing import MutableMapping

from .field import Field
from .query import Query
from .serializers import JsonSerializer
from .table import Table


class SmolStore(Iterable):
    def __init__(self, filename=None, serializer=JsonSerializer):
        self._filename = filename
        self._serializer = serializer
        if filename:
            self._load_from_file()
        else:
            self._tables = {}

    def _load_from_file(self):
        try:
            self._deserialize(self._serializer.load(self._filename))
        except FileNotFoundError:
            self._tables = {}

    def _deserialize(self, _data: MutableMapping):
        self._tables = {
            table_name: Table._deserialize(table) for table_name, table in _data.items()
        }

    def _serialize(self) -> dict:
        return {
            table_name: table._serialize() for table_name, table in self._tables.items()
        }

    def table(self, table_name="_default", fields: Iterable[Field] = None):
        if table_name in self._tables:
            return self._tables[table_name]
        else:
            table = Table(_fields=fields)
            self._tables[table_name] = table
            return table

    def __iter__(self):
        return self.table().__iter__()

    def __len__(self):
        return self.table().__len__()

    @property
    def fields(self):
        return self.table().fields

    def save(self):
        if self._filename:
            self._serializer.dump(self._filename, self._serialize())

    def delete_table(self, table_name: str):
        try:
            del self._tables[table_name]
        except KeyError:
            pass

    def insert(self, document):
        self.table().insert(document)

    def upsert(self, document, query, multiple=False):
        self.table().upsert(document, query, multiple)

    def get(self, query: Query) -> Iterator:
        return self.table().get(query)

    def first(self, query: Query):
        return self.table().first(query)

    def delete(self, query: Query):
        self.table().delete(query)

# -*- coding: utf-8 -*-
from typing import Iterable
from typing import MutableMapping

from .field import Field
from .serializers import JsonSerializer
from .table import Table


class SmolStore:
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

    def save(self):
        if self._filename:
            self._serializer.dump(self._filename, self._serialize())

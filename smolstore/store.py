# -*- coding: utf-8 -*-
import pickle
from copy import deepcopy
from threading import Lock
from typing import Iterable

from .field import Field
from .table import Table


class SmolStore:
    def __init__(self, filename=None):
        self._persistent_store = {}
        self._persistence_lock = Lock()
        self._filename = filename
        if filename:
            self._load_from_file()
        else:
            self._tables = {}

    def rollback(self):
        self._load_from_memory()

    def _load_from_memory(self):
        with self._persistence_lock:
            self._tables = deepcopy(self._persistent_store)

    def _load_from_file(self):
        try:
            with open(self._filename, "rb") as file:
                self._tables = pickle.load(file)
        except FileNotFoundError:
            self._tables = {}
        self._persistent_store = deepcopy(self._tables)

    def table(self, table_name="_default", fields: Iterable[Field] = None):
        if table_name in self._tables:
            return self._tables[table_name]
        else:
            table = Table(_lock=self._persistence_lock, _fields=fields)
            self._tables[table_name] = table
            return table

    def save(self):
        with self._persistence_lock:
            self._persistent_store = deepcopy(self._tables)
            if self._filename:
                with open(self._filename, "wb") as file:
                    pickle.dump(self._persistent_store, file)

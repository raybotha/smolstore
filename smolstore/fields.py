# -*- coding: utf-8 -*-
from typing import Iterable, MutableMapping, Mapping
from .field import Field


class Fields(Mapping):
    def __init__(self, _fields: Iterable[Field] = None, _import: MutableMapping = None):
        pass

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return "Document(%r)" % self.data

    def __str__(self):
        return self.data.__str__()

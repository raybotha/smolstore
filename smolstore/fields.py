# -*- coding: utf-8 -*-
from typing import Iterable
from typing import MutableMapping

from .field import Field


class Fields(MutableMapping):
    def __init__(self, _fields: Iterable[Field] = None):
        if not _fields:
            _fields = {}
        self.__dict__ = {field.name: field for field in _fields}

    @classmethod
    def _deserialize(cls, _data: MutableMapping):
        fields = cls()
        fields.__dict__ = {
            field_name: Field._deserialize(field) for field_name, field in _data.items()
        }
        return fields

    def _serialize(self) -> dict:
        return {field_name: field._serialize() for field_name, field in self.__dict__}

    def _register(self, document_key, field_name, old_value, new_value):
        field = self.get(field_name)
        if field is None:
            self[field_name] = Field(field_name)
        else:
            if field.indexed:
                field._add_value(document_key, new_value)
                field._remove_value(document_key, old_value)

    def __setitem__(self, key, value):
        self.__dict__.__setitem__(key, value)

    def __delitem__(self, key):
        self.__dict__.__delitem__(key)

    def __getitem__(self, key) -> Field:
        return self.__dict__.__getitem__(key)

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return self.__dict__.__len__()

    def __repr__(self):
        return "Fields(%r)" % self.__dict__

    def __str__(self):
        return self.__dict__.__str__()

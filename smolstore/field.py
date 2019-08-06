# -*- coding: utf-8 -*-
from collections import defaultdict

from .exceptions import UniqueViolation
from .query import ComparisonType
from .query import Query


class Field:
    def __init__(self, field_name=None, index=False, unique=False):
        if unique:
            index = True
        self.name = field_name
        self.indexed = index
        self.unique = unique

        self._hash_index = defaultdict(lambda: set())

    @classmethod
    def _deserialize(cls, _data):
        field = cls(**_data)
        return field

    def _serialize(self) -> dict:
        return {"field_name": self.name, "index": self.indexed, "unique": self.unique}

    def _add_value(self, document_key, value):
        hash_value = hash(value)
        if self.unique and len(self._hash_index[hash_value]) > 0:
            raise UniqueViolation
        self._hash_index[hash_value].add(document_key)

    def _remove_value(self, document_key, value):
        hash_value = hash(value)
        self._hash_index[hash_value].discard(document_key)

    def _get_keys(self, comparison_type: ComparisonType, value):
        if comparison_type == ComparisonType.EQUAL:
            hash_value = hash(value)
            return self._hash_index[hash_value]

    def __eq__(self, other):
        return Query(field=self, comparison_type=ComparisonType.EQUAL, value=other)

    def __ne__(self, other):
        return Query(field=self, comparison_type=ComparisonType.NOT_EQUAL, value=other)

    def __repr__(self):
        return "Field(%r, index=%r, unique=%r)" % (self.name, self.indexed, self.unique)

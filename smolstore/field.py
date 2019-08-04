# -*- coding: utf-8 -*-


class Field:
    def __init__(self, field_name=None, index=False, unique=False):
        if unique:
            index = True
        self.name = field_name
        self.index = index
        self.unique = unique

    @classmethod
    def _deserialize(cls, _data):
        field = cls.__new__(cls)
        field.__dict__ = _data
        return field

    def _serialize(self) -> dict:
        return self.__dict__

    def __repr__(self):
        return "Field(%s, index=%s, unique=%s)" % (self.name, self.index, self.unique)

# -*- coding: utf-8 -*-


class Field:
    def __init__(self, field_name=None, index=False, unique=False, _import=None):
        if _import:
            self.__slots__ = _import
        else:
            if unique:
                index = True
            self.name = field_name
            self.index = index
            self.unique = unique

    def __repr__(self):
        return "Field(%s, index=%s, unique=%s)" % (self.name, self.index, self.unique)

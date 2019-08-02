# -*- coding: utf-8 -*-


class Field:
    def __init__(self, field_name, index=False, unique=False):
        if unique:
            index = True
        self._field = field_name
        self._index = index
        self._unique = unique

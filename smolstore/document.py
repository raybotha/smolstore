# -*- coding: utf-8 -*-
from collections.abc import MutableMapping


class Document(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.__dict__ = {}
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        self.__dict__.__setitem__(key, value)

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __delitem__(self, key):
        self.__dict__.__delitem__(key)

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return self.__dict__.__len__()

    def __repr__(self):
        return "Document(%r)" % self.__dict__

    def __str__(self):
        return self.__dict__.__str__()

# -*- coding: utf-8 -*-
from collections.abc import MutableMapping


class Document(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.data = {}
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return "Document(%r)" % self.data

    def __str__(self):
        return self.data.__str__()

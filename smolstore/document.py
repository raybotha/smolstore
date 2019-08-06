# -*- coding: utf-8 -*-
from typing import Mapping
from typing import MutableMapping

from .exceptions import ReservedKey


class Document(MutableMapping):
    def __init__(self, _table, _document_key, mapping):
        self.__dict__["_reserved_keys"] = {
            "_reserved_keys",
            "_document_table",
            "_document_key",
        }
        self.__dict__["_document_table"] = _table
        self.__dict__["_document_key"] = _document_key
        self.update(mapping)

    def _set_item(self, key, value):
        if key in self["_reserved_keys"]:
            raise ReservedKey("'%s' is a reserved document key in smolstore" % key)

        if not isinstance(value, Mapping):
            old_value = self.get(key)
            self["_document_table"].fields._register(
                document_key=self["_document_key"],
                field_name=key,
                old_value=old_value,
                new_value=value,
            )

        self.__dict__[key] = value

    def _del_item(self, key):
        print("deleted")
        if key in self["_reserved_keys"]:
            raise ReservedKey("'%s' is a reserved document key in smolstore" % key)

        self["_document_table"].fields._unregister(
            document_key=self["_document_key"], field_name=key, value=self.get(key)
        )

        del self.__dict__[key]

    def __setattr__(self, key, value):
        self._set_item(key, value)

    def __delattr__(self, item):
        self._del_item(item)

    def __setitem__(self, key, value):
        self._set_item(key, value)

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def __delitem__(self, key):
        self._del_item(key)

    def __iter__(self):
        for item in self.__dict__:
            if item not in self["_reserved_keys"]:
                yield item

    def __len__(self):
        return len(dict(self))

    def __repr__(self):
        return "Document(%r)" % dict(self)

    def __str__(self):
        return dict(self).__str__()

    def delete(self):
        self["_document_table"]._delete_document(self["_document_key"])

# -*- coding: utf-8 -*-


class SmolStoreException(Exception):
    pass


class UniqueViolation(SmolStoreException):
    pass


class ReservedKey(SmolStoreException):
    pass
